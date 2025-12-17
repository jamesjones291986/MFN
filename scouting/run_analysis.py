#!/usr/bin/env python3
"""
Wrapper script to run team analysis with better error handling
"""

import subprocess
import sys
import os
from pathlib import Path

def run_team_analysis():
    """Run the team analysis with proper environment setup."""
    
    # Get the script arguments
    args = sys.argv[1:]  # Skip the script name
    
    # Build the command
    script_path = "team_specific_analysis/team_specific_success_analyzer.py"
    cmd = [sys.executable, script_path] + args
    
    print(f"🏈 Running team analysis...")
    print(f"Command: {' '.join(cmd)}")
    print("=" * 50)
    
    try:
        # Run the script in a clean environment
        env = os.environ.copy()
        
        # Remove any conflicting Python paths
        if 'PYTHONPATH' in env:
            del env['PYTHONPATH']
        
        # Run the script
        result = subprocess.run(cmd, env=env, cwd=Path(__file__).parent)
        return result.returncode
        
    except Exception as e:
        print(f"❌ Error running analysis: {e}")
        return 1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 run_analysis.py --opponent TEAM --league USFL --season 2018")
        sys.exit(1)
    
    exit_code = run_team_analysis()
    sys.exit(exit_code)