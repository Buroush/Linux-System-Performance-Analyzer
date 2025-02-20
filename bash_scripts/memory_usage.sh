#!/bin/bash
set -euo pipefail
trap 'echo "An error occurred at line $LINENO"; exit 1' ERR
# Redirect all output to a log file, while still displaying it on the console
exec > >(tee -a ./logs/system_monitor.log) 2>&1

# memory_usage.sh - Collect Memory usage

# Get total and used memory from 'free' command
total_mem=$(free -m | awk '/^Mem:/{print $2}')
used_mem=$(free -m | awk '/^Mem:/{print $3}')
mem_usage=$(( (used_mem * 100) / total_mem ))

echo "Current Memory usage: ${mem_usage}%"

