#!/usr/bin/env python3
"""
MFN Gameplan Generator
======================

Main entry point for the automated gameplan generator system.
This provides a cleaner interface to the underlying functionality.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append('/Users/jamesjones/projects/mfn/scouting')

from automated_gameplan_generator import main

if __name__ == "__main__":
    main()