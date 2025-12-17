#!/usr/bin/env python3
"""
Standalone Team Analysis Tool
=============================

Self-contained version that avoids import conflicts.
"""

import subprocess
import sys
import os
from pathlib import Path

def install_and_import():
    """Install packages and import them safely."""
    
    # Install packages if needed
    try:
        import pandas as pd
        print("✅ Pandas already available")
    except ImportError:
        print("📦 Installing pandas...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas>=1.3.0"])
        import pandas as pd
        print("✅ Pandas installed and imported")
    
    try:
        import numpy as np
        print("✅ Numpy already available") 
    except ImportError:
        print("📦 Installing numpy...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy>=1.20.0"])
        import numpy as np
        print("✅ Numpy installed and imported")
    
    return pd, np

def main():
    """Run the analysis using subprocess to avoid import conflicts."""
    
    if len(sys.argv) < 4:
        print("Usage: python3 team_analysis.py --opponent TEAM --league USFL --season 2018")
        sys.exit(1)
    
    print("🏈 TEAM ANALYSIS TOOL")
    print("=" * 30)
    
    # Install dependencies
    print("🔧 Checking dependencies...")
    try:
        pd, np = install_and_import()
    except Exception as e:
        print(f"❌ Dependency error: {e}")
        sys.exit(1)
    
    # Build command for the actual analysis
    script_path = Path(__file__).parent / "team_specific_analysis" / "team_specific_success_analyzer.py"
    
    # Get all arguments except script name
    args = sys.argv[1:]
    cmd = [sys.executable, str(script_path)] + args
    
    print(f"🚀 Running analysis...")
    print(f"Command: {' '.join(cmd)}")
    print()
    
    # Run in a completely clean environment
    env = os.environ.copy()
    
    # Remove Python path conflicts
    env.pop('PYTHONPATH', None)
    
    # Set clean working directory
    cwd = Path(__file__).parent
    
    try:
        # Run the subprocess
        result = subprocess.run(
            cmd,
            env=env,
            cwd=cwd,
            text=True
        )
        return result.returncode
        
    except Exception as e:
        print(f"❌ Error running analysis: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)