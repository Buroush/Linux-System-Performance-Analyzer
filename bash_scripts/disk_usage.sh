#!/bin/bash
set -euo pipefail
trap 'echo "An error occurred at line $LINENO"; exit 1' ERR
# Redirect all output to a log file, while still displaying it on the console
exec > >(tee -a ./logs/system_monitor.log) 2>&1

# disk_usage.sh - Collect Disk usage

# Get disk usage percentage for the root (/) filesystem
disk_usage=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')

echo "Current Disk usage: ${disk_usage}%"

