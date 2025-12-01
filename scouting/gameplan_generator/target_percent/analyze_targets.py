#!/usr/bin/env python3
"""
Target Analyzer Wrapper
========================

Simple wrapper for the target analyzer to make it easier to run from the gameplan_generator directory.

Usage:
    python target_percent/analyze_targets.py --team SJS --league USFL --season 2018
    python target_percent/analyze_targets.py --standard-playbook
"""

import sys
import os
from pathlib import Path

# Add the target_percent directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from target_analyzer import main

if __name__ == "__main__":
    sys.exit(main())