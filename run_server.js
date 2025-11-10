import fs from 'fs';
import { execSync } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

// --- Setup paths ---
// This part is perfect, it correctly finds the script's directory.
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const nodeModulesDir = path.join(__dirname, 'node_modules');
const distDir = path.join(__dirname, 'dist');
const serverScriptPath = path.join(distDir, 'server.js');
const buildInfoPath = path.join(__dirname, 'build_info.json');
const geminiExtensionPath = path.join(__dirname, 'gemini-extension.json');

function getExtensionVersion() {
    const extensionJson = JSON.parse(fs.readFileSync(geminiExtensionPath, 'utf8'));
    return extensionJson.version;
}

function hasVersionChanged() {
    if (!fs.existsSync(buildInfoPath)) {
        return true;
    }
    try {
        const buildInfo = JSON.parse(fs.readFileSync(buildInfoPath, 'utf8'));
        const currentVersion = getExtensionVersion();
        return buildInfo.lastBuildVersion !== currentVersion;
    } catch (error) {
        console.error('Error reading or parsing build_info.json:', error);
        return true; // Force a rebuild if the file is corrupt
    }
}

function updateBuildInfo() {
    try {
        const currentVersion = getExtensionVersion();
        const buildInfo = { lastBuildVersion: currentVersion };
        fs.writeFileSync(buildInfoPath, JSON.stringify(buildInfo, null, 2));
        console.log(`Updated build_info.json to version ${currentVersion}`);
    } catch (error) {
        console.error('Error updating build_info.json:', error);
    }
}

// --- Dependency and Build Check ---
// A more reliable check is to look for node_modules and dist separately.
try {
    // 1. Check if dependencies are installed.
    if (!fs.existsSync(nodeModulesDir)) {
        console.log('node_modules directory not found. Running "npm install"...');
        execSync('npm install', { cwd: __dirname, stdio: 'inherit' });
    }

    // 2. Check if the project has been built or if the version has changed.
    if (!fs.existsSync(distDir) || hasVersionChanged()) {
        if (!fs.existsSync(distDir)) {
            console.log('dist directory not found. Running "npm run build"...');
        } else {
            console.log('Extension version has changed. Running "npm run build"...');
        }
        execSync('npm run build', { cwd: __dirname, stdio: 'inherit' });
        updateBuildInfo(); // Update build info after a successful build
    }

    console.log('Setup is complete. Starting server...');

    // --- Start the Server ---    
    execSync(`node "${serverScriptPath}"`, { stdio: 'inherit' });

} catch (error) {
    console.error('An error occurred during the setup or server execution:', error);
    process.exit(1);
}