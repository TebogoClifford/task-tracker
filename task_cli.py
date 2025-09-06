#!/usr/bin/env python3
"""
Task Tracker CLI
A simple command-line tool to manage tasks using a JSON file.
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timezone

# File to store tasks
TASKS_FILE = Path("tasks.json")

# Helper: current UTC time in ISO format
def now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

# Ensure the file exists with an empty list
def ensure_file():
    if not TASKS_FILE.exists():
        with TASKS_FILE.open("w") as f:
            json.dump([], f)

# Load tasks (list of dicts) from file
def load_tasks():
    ensure_file()
    with TASKS_FILE.open("r") as f:
        return json.load(f)

# Save tasks (overwrite the file)
def save_tasks(tasks):
    with TASKS_FILE.open("w") as f:
        json.dump(tasks, f, indent=2)
