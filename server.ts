/**
 * @license
 * Copyright 2025 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */

import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';
import * as fs from 'fs/promises';
import * as path from 'path';
import { fileURLToPath } from 'url';
import { exec } from 'child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const server = new McpServer({
  name: 'prompt-server',
  version: '1.0.0',
});

server.registerTool(
  'logic_init',
  {
    description:
      'Initializes Logic-Officer by creating architectural markdown files.',
    inputSchema: z.object({}).shape,
  },
  async () => {
    const templatesDir = path.join(__dirname, '..', 'templates');
    const logicDir = path.join(process.cwd(), '.logic');

    try {
      await fs.mkdir(logicDir, { recursive: true });

      const filesToCopy = [
        'architectural_principles.md',
        'project_architectural_decisions.md',
        'code_review_guidelines.md',
        'coding_conventions.md'
      ];

      for (const file of filesToCopy) {
        const src = path.join(templatesDir, file);
        const dest = path.join(logicDir, file);
        await fs.copyFile(src, dest);
      }

      return {
        content: [
          {
            type: 'text',
            text: 'Logic-Officer initialized successfully.',
          },
        ],
      };
    } catch (error: any) {
      return {
        content: [
          {
            type: 'text',
            text: `Error initializing Logic-Officer: ${error.message}`,
          },
        ],
      };
    }
  },
);

server.registerTool(
  'check-staged',
  {
    description: 'Checks if there are any staged files in the current git repository.',
    inputSchema: z.object({}).shape,
  },
  async () => {
    return new Promise((resolve) => {
      exec('git diff --cached --quiet', (error) => {
        if (error) {
          resolve({
            content: [
              {
                type: 'text',
                text: 'Files are staged and ready for commit.',
              },
            ],
          });
        } else {
          resolve({
            content: [
              {
                type: 'text',
                text: "No staged files found. Please use 'git add' first.",
              },
            ],
          });
        }
      });
    });
  },
);


console.log("---")
const transport = new StdioServerTransport();
await server.connect(transport);
