#!/usr/bin/env python3
"""
Setup script for MFN Scouting Tools
===================================

Installs required dependencies for the MFN scouting analysis tools.
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install packages from requirements.txt"""
    
    print("🏈 MFN Scouting Tools Setup")
    print("=" * 30)
    
    # Check if we're in the right directory
    current_dir = Path(__file__).parent
    requirements_file = current_dir / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ requirements.txt not found!")
        print(f"   Expected: {requirements_file}")
        return False
    
    print(f"📦 Installing dependencies from {requirements_file}")
    
    try:
        # Install requirements
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ], check=True, capture_output=True, text=True)
        
        print("✅ Dependencies installed successfully!")
        print(f"   Output: {result.stdout.strip()}")
        
        # Test imports
        print("\n🧪 Testing imports...")
        test_imports()
        
        print("\n🎯 Setup complete! You can now run:")
        print("   python team_specific_analysis/team_specific_success_analyzer.py --opponent MIC --league USFL --season 2018")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies:")
        print(f"   Error: {e}")
        print(f"   Output: {e.stderr}")
        return False

def test_imports():
    """Test that required packages can be imported."""
    
    packages = [
        ('pandas', 'pd'),
        ('numpy', 'np'),
        ('gspread', None),
        ('google.auth', None),
    ]
    
    for package, alias in packages:
        try:
            if alias:
                exec(f"import {package} as {alias}")
            else:
                exec(f"import {package}")
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ⚠️  {package} (optional)")

if __name__ == "__main__":
    success = install_requirements()
    sys.exit(0 if success else 1)