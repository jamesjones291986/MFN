#!/usr/bin/env python3
"""Test script to isolate the numpy import issue"""

import sys
import os

print("Python version:", sys.version)
print("Python executable:", sys.executable)
print("Current working directory:", os.getcwd())

try:
    print("Attempting to import numpy...")
    import numpy
    print("✅ Numpy imported successfully:", numpy.__version__)
except Exception as e:
    print("❌ Numpy import failed:", e)
    sys.exit(1)

try:
    print("Attempting to import pandas...")
    import pandas
    print("✅ Pandas imported successfully:", pandas.__version__)
except Exception as e:
    print("❌ Pandas import failed:", e)
    sys.exit(1)

print("All imports successful!")