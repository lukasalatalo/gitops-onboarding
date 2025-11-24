#!/usr/bin/env python3
"""
Sample Python script for nightly cronjob
This script runs every minute (or as scheduled)
"""

import sys
import os
import json
from datetime import datetime
from pathlib import Path

def log(message: str, level: str = "INFO"):
    """Log a message with timestamp"""
    timestamp = datetime.utcnow().isoformat() + "Z"
    print(f"[{timestamp}] [{level}] {message}", flush=True)

def main():
    """Main function"""
    log("=" * 50)
    log("CronJob Python Script Started")
    log("=" * 50)
    
    # Example: Get environment variables
    log(f"Python version: {sys.version}")
    log(f"Working directory: {os.getcwd()}")
    
    # Example: Check if running in Kubernetes
    if os.path.exists("/var/run/secrets/kubernetes.io"):
        log("Running in Kubernetes environment")
    
    # Example: Perform some tasks
    log("Performing maintenance tasks...")
    
    # Example: Simulate some work
    import time
    time.sleep(1)  # Simulate work
    
    # Example: Generate a simple report
    report = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": "success",
        "tasks_completed": [
            "Task 1: System check",
            "Task 2: Data processing",
            "Task 3: Cleanup operations"
        ]
    }
    
    log(f"Report: {json.dumps(report, indent=2)}")
    
    # Example: Check system resources (if available)
    try:
        import psutil
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        log(f"CPU usage: {cpu_percent}%")
        log(f"Memory usage: {memory.percent}% ({memory.used / 1024**3:.2f} GB / {memory.total / 1024**3:.2f} GB)")
    except ImportError:
        log("psutil not available, skipping resource monitoring", "WARNING")
    
    log("=" * 50)
    log("CronJob Python Script Completed Successfully")
    log("=" * 50)
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        log(f"Error occurred: {str(e)}", "ERROR")
        import traceback
        log(traceback.format_exc(), "ERROR")
        sys.exit(1)

