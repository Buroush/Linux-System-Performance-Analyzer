#!/bin/bash
set -euo pipefail
trap 'echo "An error occurred at line $LINENO"; exit 1' ERR
# Redirect all output to a log file, while still displaying it on the console
exec > >(tee -a ./logs/system_monitor.log) 2>&1

# io_usage.sh - Collect I/O usage, excluding loop devices

io_usage=$(iostat -dx 1 1 | awk '$1 !~ /loop/ {print $1, $14}' | column -t)

echo "Disk I/O usage (device and utilization %):"
echo "$io_usage"

