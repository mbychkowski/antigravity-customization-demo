#!/usr/bin/env python3
"""
Antigravity Pre-Tool Hook: Validates sqlite3 commands before execution.
Reads tool invocation data from stdin and outputs JSON decision.
"""

import sys
import json
import os

def main():
    # Parse stdin JSON payload sent by Antigravity runtime
    try:
        raw_input = sys.stdin.read()
        payload = json.loads(raw_input) if raw_input else {}
    except Exception:
        payload = {}

    # Extract command string (e.g. "sqlite3 blog.db < migrations/001_add_status.sql")
    command = payload.get("tool_input", {}).get("command", "")
    cmd_lower = command.lower()

    # Check 1: Block write/modification commands if backup file is missing
    is_modifying_op = any(op in cmd_lower for op in ["<", "insert", "update", "drop", "alter", "delete", "create"])

    if is_modifying_op and not os.path.exists("blog.db.bak"):
        return_decision(
            decision="deny",
            reason="[HOOK BLOCKED] Missing safety backup! 'blog.db.bak' does not exist. "
                   "You must create a backup copy using 'cp blog.db blog.db.bak' before executing database modifications."
        )

    # Check 2: Block raw unscripted DROP TABLE commands
    if "drop table" in cmd_lower and ".sql" not in cmd_lower:
        return_decision(
            decision="deny",
            reason="[HOOK BLOCKED] Direct 'DROP TABLE' statements via CLI are prohibited by safety policy. "
                   "All schema modifications must be executed through migration .sql files."
        )

    # Check 3: If running a migration file, verify a corresponding .down.sql script exists
    if "<" in command and ".up.sql" in command:
        sql_file = command.split("<")[-1].strip().strip('"').strip("'")
        down_file = sql_file.replace(".up.sql", ".down.sql")

        if not os.path.exists(down_file):
            return_decision(
                decision="deny",
                reason=f"[HOOK BLOCKED] Unsafe migration missing rollback script! "
                       f"Found '{sql_file}' but could not find matching '{down_file}'."
            )

    # If all checks pass, approve execution
    return_decision(decision="approve")

def return_decision(decision: str, reason: str = ""):
    output = {"decision": decision}
    if reason:
        output["reason"] = reason
    print(json.dumps(output))
    sys.exit(0)

if __name__ == "__main__":
    main()
```
,Description:
