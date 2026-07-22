## 1. Write the Rule to protect blog.db

```
migration-safety.md
```

```
I need to add a status column to blog.db. Just write a quick script that drops the existing posts table and recreates it with id, title, body, created_at, and status NOT NULL.
```

## 2. Show me how to write the Antigravity Skill skills/generate-schema-diff.md to inspect blog.db and draft the migration SQL.

```
/generate-schema-diff Add an author_id INTEGER column and a tags table to blog.db
```

or

```
Inspect blog.db and draft a migration to add an author_id column to posts.
```