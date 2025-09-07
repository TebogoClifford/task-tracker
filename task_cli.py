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
        
def update_task(task_id,new_description):
    tasks = load_tasks()
    
    for t in tasks:
        if t["ID"] == task_id:
            t["description"] = new_description 
            t["updatedAt"] = now() 
            save_tasks(tasks)
            print(f"task updated successfully (ID: {task_id})")
            return
    print(f"Error: Task with ID {task_id} not found")
            
def delete_task(task_id):
    tasks = load_tasks()
    
    new_tasks = [t for t in tasks if t["id"] != task_id]
    if len(new_tasks) == len(tasks):
        print(f"error: task ID {task_id} not found")
        return  
    save_tasks(new_tasks)
    print(f"task deleted successfully (ID: {task_id})")
 
def mark_task(task_id, status):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["status"] = status
            t["updatedAt"] = now()
            save_tasks(tasks)
            print(f"Task marked as {status} (ID: {task_id})")
            return
    print(f"Error: Task with ID {task_id} not found")
    
def main():
    if len(sys.argv) < 2:
        print("Usage: task-cli <command> [arguments]")
        return

    command = sys.argv[1]

    if command == "add":
        description = " ".join(sys.argv[2:])
        add_task(description)

    elif command == "list":
        status = sys.argv[2] if len(sys.argv) > 2 else None
        list_tasks(status)

    elif command == "update":
        if len(sys.argv) < 4:
            print("Usage: task-cli update <id> <new description>")
            return
        task_id = int(sys.argv[2])
        new_description = " ".join(sys.argv[3:])
        update_task(task_id, new_description)

    elif command == "delete":
        if len(sys.argv) < 3:
            print("Usage: task-cli delete <id>")
            return
        task_id = int(sys.argv[2])
        delete_task(task_id)

    elif command == "mark-in-progress":
        task_id = int(sys.argv[2])
        mark_task(task_id, "in-progress")

    elif command == "mark-done":
        task_id = int(sys.argv[2])
        mark_task(task_id, "done")

    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()

    
    