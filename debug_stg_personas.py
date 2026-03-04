import sys
import os

# Set project root in path
project_root = '/Users/educifuentes/code/greenlab-censos'
sys.path.append(project_root)

from models.staging.censo_2024._stg_censo_2024__personas import stg_censo_2024__personas

try:
    print("Running stg_censo_2024__personas()...")
    df = stg_censo_2024__personas()
    print("Success!")
    print(df.head())
except Exception as e:
    print(f"Failed: {e}")
