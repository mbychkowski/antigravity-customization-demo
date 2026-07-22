---
name: generate-schema-diff
description: Inspects SQLite schema using bundled tools and drafts paired up/down SQL migration scripts.
globs: ["*.db", "migrations/*.sql"]
---
# Skill: Generate Schema Diff & Migration SQL

Use this skill when asked to update, alter, or add new features to a database.

## Execution Procedure

### Step 1: Run Inspection Tool
Execute the skill's bundled inspection script against the target database:

```bash
python3 .agents/skills/generate-schema-diff/scripts/inspect_schema.py blog.db