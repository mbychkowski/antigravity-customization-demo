import sqlite3

# 1. Connect to blog.db (creates the file if it doesn't exist)
conn = sqlite3.connect("blog.db")
cursor = conn.cursor()

# 2. Create the initial v1 schema (posts table only)
cursor.execute("""
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

# 3. Seed initial sample data
sample_posts = [
    (
        "Getting Started with Antigravity",
        "Antigravity plugins combine Rules, Skills, Workflows, Hooks, and Sidecars into a single package."
    ),
    (
        "Why SQLite is Perfect for Prototypes",
        "SQLite requires zero server setup, runs in a single local file, and is standard in Python."
    ),
    (
        "Building a Safe Migration Sentinel",
        "Automating database guardrails prevents catastrophic schema breaking changes in production."
    )
]

cursor.executemany("""
    INSERT INTO posts (title, body) VALUES (?, ?);
""", sample_posts)

# 4. Commit changes and close connection
conn.commit()
conn.close()

print("✅ Successfully created 'blog.db' and seeded initial posts!")