---
trigger: always
globs: ["**/*.sql", "migrations/**", "blog.db"]
---
# SQLite Migration Safety Rules

You are operating under strict database safety constraints for `blog.db`. Follow these rules without exception during any database schema modification or migration task:

## 1. Zero Data Loss Policy
- **Never execute unrecoverable commands:** Do NOT issue `DROP TABLE` or `DELETE FROM` on primary tables unless executing a structured, temporary-table migration strategy.
- **Row Count Preservation:** Before applying any schema change, record the current row count (`SELECT COUNT(*) FROM posts;`). After applying the migration, verify that the row count matches the pre-migration count.

## 2. Mandatory Backup Prerequisites
- **Backup Verification:** Before running any SQL migration script against `blog.db`, verify that a backup copy named `blog.db.bak` exists.
- **Auto-Backup:** If `blog.db.bak` is missing, run `cp blog.db blog.db.bak` before executing any write commands.

## 3. SQLite Schema Constraints
- **Table Recreation Pattern:** SQLite limits direct `ALTER TABLE` operations. If a schema change requires table recreation:
  1. Create the new table (e.g., `posts_v2`).
  2. Copy existing data: `INSERT INTO posts_v2 (id, title, body, created_at) SELECT id, title, body, created_at FROM posts;`.
  3. Drop the old `posts` table and rename `posts_v2` to `posts`.
- **Default Values:** When adding new `NOT NULL` columns (such as `status`), always specify a `DEFAULT` value (e.g., `'draft'`) so existing rows remain valid.

## 4. Reversibility Requirements
- **Paired Rollbacks:** Every `*.up.sql` file created inside `migrations/` MUST have a corresponding `*.down.sql` file capable of cleanly restoring the previous schema without losing existing posts.