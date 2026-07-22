-- Migration UP: Add author_email, author, status to posts, and create tags table

-- 1. Create the new posts table with desired schema
CREATE TABLE posts_v2 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    author TEXT DEFAULT 'Anonymous',
    author_email TEXT,
    status TEXT NOT NULL DEFAULT 'draft'
);

-- 2. Copy existing data from old posts table
INSERT INTO posts_v2 (id, title, body, created_at)
SELECT id, title, body, created_at FROM posts;

-- 3. Drop the old table
DROP TABLE posts;

-- 4. Rename the new table to posts
ALTER TABLE posts_v2 RENAME TO posts;

-- 5. Create the tags table
CREATE TABLE tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY (post_id) REFERENCES posts (id) ON DELETE CASCADE,
    UNIQUE(post_id, name)
);
