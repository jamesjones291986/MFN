#!/bin/bash

# MFN Automated Gameplan Wrapper Script
# This script isolates the Python environment to avoid numpy import conflicts

# Clear any problematic environment variables
unset PYTHONPATH
export PYTHONDONTWRITEBYTECODE=1

# Change to a clean directory temporarily to avoid any local conflicts
cd /tmp

# Run the script with absolute paths
exec python3 /Users/jamesjones/projects/mfn/automated_gameplan.py "$@"