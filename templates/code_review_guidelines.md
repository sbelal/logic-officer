# Code Review Guidelines

## Priority Focus Areas
When reviewing code I will focus on the following areas.

### 🔴 Critical (Must Address)
- **Security vulnerabilities**: SQL injection, XSS, authentication bypass
- **Data integrity issues**: Race conditions, data loss scenarios
- **Breaking changes**: API compatibility, database migrations
- **Performance bottlenecks**: N+1 queries, inefficient algorithms

### 🟡 Important (Should Address)
- **Error handling**: Missing try-catch, unhandled edge cases
- **Testing**: Missing test coverage for new logic
- **Code duplication**: DRY violations across files
- **Complex logic**: Methods >50 lines, deeply nested conditionals

### 🟢 Nice-to-Have (Suggestions)
- **Naming improvements**: Unclear variable/function names.  Ideally a function name describes the purpose of operation.
- **Code organization**: Extract reusable utilities or service, better file structure
- **Documentation**: Missing comments for complex logic
- **Performance optimizations**: Potential caching, batching, multithreading

## Review Structure

For each file reviewed, provide:
1.  **Summary**: Brief overview of changes
2.  **Issues**: Specific problems with line references. Mark severity: 🔴 Critical, 🟡 Important, 🟢 Nice-to-Have
3.  **Positives**: What was well-done (build confidence)
4.  **Coding convention violations**: Brief overview of coding conventions broken, if found
5.  **Architectural violations**: Brief overview of architectural principles or project architecture decision violations, if found
6.  **Refactoring**: Structural improvements with examples if needed. Identify code that could be extracted out as utility functions or new service classes.
7.  **Recommendations**: Actionable next steps

Once the review of each file is complete, add an overall assessment section. This section should state [or specify] whether the code changes align with the JIRA ticket.

## Team Conventions

### Commit Messages
- Follow format: [branch-name] Brief description
- Use imperative mood

### Testing Requirements
- Unit tests for all business logic
- Integration tests for API endpoints
- Minimum 80% code coverage

### Documentation
- README.md updated for new features
- Architecture.md updated with new decisions documented

## Continuous Improvement

This document is living and should evolve based on:
- Feedback from code reviews
- Recurring issues found in production
- New technologies and best practices adopted by the team

**Last Updated**: [Date]
**Recent Improvements**: [Track changes here]