---
name: safe-migrate
description: Orchestrates an end-to-end safe SQLite database migration with backup, hook validation, and row verification.
---
# Workflow: Safe Database Migration Pipeline

Follow these steps in strict sequence whenever the user requests a database migration or triggers `/safe-migrate`.

## Step 1: Draft Migration Scripts
Invoke the `/generate-schema-diff` skill with the user's requested schema changes to generate:
- The next sequential `migrations/<NNN>_<description>.up.sql`
- The corresponding `migrations/<NNN>_<description>.down.sql`

## Step 2: Ensure Safety Backup
Before executing any SQL, check if `blog.db.bak` exists:
- If `blog.db.bak` does not exist, run `cp blog.db blog.db.bak`.
- Verify the backup file was created successfully.

## Step 3: Record Pre-Migration Metrics
Execute a pre-flight count query on primary tables to establish baseline metrics:
```bash
python3 -c "import sqlite3; conn=sqlite3.connect('blog.db'); print('PRE_COUNT:', conn.cursor().execute('SELECT COUNT(*) FROM posts;').fetchone()[0]); conn.close()"
```

## Step 4: Apply UP Migration
Execute the newly drafted upgrade SQL script to apply the schema changes:
```bash
sqlite3 blog.db < migrations/<NNN>_<description>.up.sql
```

## Step 5: Test Rollback DOWN and Re-apply UP
To guarantee the migration is fully reversible, perform a live rollback and re-apply cycle:
1. Run the rollback script:
   ```bash
   sqlite3 blog.db < migrations/<NNN>_<description>.down.sql
   ```
2. Verify the row count matches the pre-migration count and that the schema is safely reverted:
   ```bash
   python3 -c "import sqlite3; conn=sqlite3.connect('blog.db'); print('ROLLBACK_COUNT:', conn.cursor().execute('SELECT COUNT(*) FROM posts;').fetchone()[0]); conn.close()"
   ```
3. Re-apply the upgrade script:
   ```bash
   sqlite3 blog.db < migrations/<NNN>_<description>.up.sql
   ```

## Step 6: Summary Report
1. Verify the final post-migration row count:
   ```bash
   python3 -c "import sqlite3; conn=sqlite3.connect('blog.db'); print('POST_COUNT:', conn.cursor().execute('SELECT COUNT(*) FROM posts;').fetchone()[0]); conn.close()"
   ```
2. Report the final database schema and state of the posts table.