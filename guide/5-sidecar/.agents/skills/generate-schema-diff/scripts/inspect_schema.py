#!/usr/bin/env python3
"""
Inspects an SQLite database file and outputs structured schema info.
Usage: python3 inspect_schema.py <db_path>
"""

import sys
import sqlite3
import json

def inspect_db(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Get all non-internal tables
        tables = [t[0] for t in cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
        ).fetchall()]

        schema = {}
        for table in tables:
            cols = cursor.execute(f"PRAGMA table_info({table});").fetchall()
            schema[table] = [
                {
                    "cid": col[0],
                    "name": col[1],
                    "type": col[2],
                    "notnull": bool(col[3]),
                    "dflt_value": col[4],
                    "pk": bool(col[5])
                }
                for col in cols
            ]

        conn.close()
        return schema
    except Exception as e:
        print(f"Error inspecting database {db_path}: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 inspect_schema.py <path_to_sqlite_db>")
        sys.exit(1)

    db_file = sys.argv[1]
    result = inspect_db(db_file)
    print(json.dumps(result, indent=2))
