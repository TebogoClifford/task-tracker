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

def add_task(description):
    task = load_tasks()
    
    #finds the max idno 
    next_id = max((t['id'] for t in task), default=0) + 1
    
    new_task = {
        "id": next_id,
        "description": description,
        "status": "todo",
        "createdAt": now(),
        "updatedAt": now()
    }
    
    task.append(new_task)
    save_tasks(task)
    print(f"task added successfully (ID: {next_id})")
    
def list_tasks(status=none):
    task = load_tasks() 
    
    if status:
        tasks = [t for t in tasks if t["status"] == status]
        
    if not tasks:
        print("no tasks") 
        return 
    
    print(f"{'ID':<3}{'status':<12}{'DESCRIPTION':<30}{'UPDATED'}")
    print("-" * 70)
    
    for t in tasks:
        print(f"{t['id']:<3} {t['status']:<12} {t['description']:<30} {t['updatedAt']}")