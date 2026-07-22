#!/usr/bin/env python3
"""
Antigravity Sidecar: Asynchronously monitors blog.db health in the background.
Writes status alerts to .agent/runtime/sidecar_alerts.json.
"""

import os
import time
import sqlite3
import json

DB_PATH = "blog.db"
ALERT_FILE = ".agent/runtime/sidecar_alerts.json"

def check_health():
    alerts = []

    if not os.path.exists(DB_PATH):
        return

    # 1. Check DB file size (Flag if unexpectedly bloated)
    size_mb = os.path.getsize(DB_PATH) / (1024 * 1024)
    if size_mb > 50:
        alerts.append({"level": "WARN", "msg": f"Database file size is large: {size_mb:.2f}MB"})

    # 2. Check Write-Ahead Log (WAL) bloat
    wal_path = f"{DB_PATH}-wal"
    if os.path.exists(wal_path):
        wal_mb = os.path.getsize(wal_path) / (1024 * 1024)
        if wal_mb > 10:
            alerts.append({"level": "WARN", "msg": f"WAL log growing: {wal_mb:.2f}MB. Recommend running PRAGMA wal_checkpoint;"})

    # 3. Check for open database locks
    try:
        conn = sqlite3.connect(DB_PATH, timeout=1.0)
        conn.execute("PRAGMA quick_check;")
        conn.close()
    except sqlite3.OperationalError as e:
        alerts.append({"level": "ERROR", "msg": f"Database lock detected: {e}"})

    # Write status to runtime folder for Antigravity main loop to read
    os.makedirs(os.path.dirname(ALERT_FILE), exist_ok=True)
    with open(ALERT_FILE, "w") as f:
        json.dump({"timestamp": time.time(), "alerts": alerts}, f, indent=2)

if __name__ == "__main__":
    while True:
        check_health()
        time.sleep(5)