-- Migration DOWN: Rollback author_email, author, status from posts, and drop tags table

-- 1. Drop the tags table
DROP TABLE IF EXISTS tags;

-- 2. Create the old posts table structure (v1)
CREATE TABLE posts_v1 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Copy data back, ignoring the new columns
INSERT INTO posts_v1 (id, title, body, created_at)
SELECT id, title, body, created_at FROM posts;

-- 4. Drop current posts table
DROP TABLE posts;

-- 5. Rename v1 table back to posts
ALTER TABLE posts_v1 RENAME TO posts;
