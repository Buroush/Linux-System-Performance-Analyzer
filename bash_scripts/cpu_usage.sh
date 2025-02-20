#!/bin/bash
set -euo pipefail
trap 'echo "An error occurred at line $LINENO"; exit 1' ERR
# Redirect all output to a log file, while still displaying it on the console
exec > >(tee -a ./logs/system_monitor.log) 2>&1

# cpu_usage.sh - Collect CPU usage

# Using 'top' in batch mode to get the current CPU usage,
# 'grep' to filter the CPU line, 'awk' to sum the user and system percentages,
# and 'cut' to remove the decimal part.
cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2 + $4}' | cut -d'.' -f1)

echo "Current CPU usage: ${cpu_usage}%"
