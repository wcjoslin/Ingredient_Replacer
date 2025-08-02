# COPILOT_INSTRUCTIONS Template

## Purpose

This markdown file serves as a template for development plans and workflow instructions for all tasks derived from Notion via the NotionMCP.

---

## Usage Instructions

1. **Always Use This Template for Notion Tasks**
   - Every time a Notion task is read from the NotionMCP, Cline must use this template to create a detailed development plan before any coding or implementation begins.
   - The plan should include: requirements, step-by-step breakdown, testing, documentation, and review/merge strategy.

2. **Pull Request Workflow (No Direct Main Commits)**
   - **Never commit directly to the `main` branch.**
   - For every feature, bugfix, or documentation update:
     1. Create a new branch from `main` (e.g., `feature/your-task-name`).
     2. Make and commit your changes to this branch.
     3. Push the branch to GitHub.
     4. Open a Pull Request (PR) from your branch into `main`.
     5. Ensure all tests pass and request review if needed.
     6. Only merge the PR after review and successful checks.
   - This workflow helps prevent repo corruption and ensures all changes are reviewed and recoverable.

---

## Example Development Plan

1. **Task Summary**
   - Briefly describe the task or feature.

2. **Requirements**
   - List all requirements and acceptance criteria.

3. **Implementation Steps**
   - Step-by-step breakdown of the work to be done.

4. **Testing**
   - Outline unit, integration, and manual testing steps.

5. **Documentation**
   - Note any README/API doc updates required.

6. **Pull Request**
   - Confirm that all changes will be made in a feature branch and merged via PR.

---

## Notes

- Always refer to this template before starting any new development task from Notion.
- If you have questions about the workflow, ask the project maintainer.
