#!/usr/bin/env python3
"""
Debug script to check what columns are available in the USFL 2011 data
"""

import pandas as pd
import sys
sys.path.append('.')
from util import Config

# Load the feather file
feather_path = f"{Config.seasons}/USFL_2011.feather"
df = pd.read_feather(feather_path)

print("Columns available in USFL_2011.feather:")
print(df.columns.tolist())
print(f"\nShape: {df.shape}")
print(f"\nFirst few rows:")
print(df.head(2))