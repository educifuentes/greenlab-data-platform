import pandas as pd
import os
import pyarrow.parquet as pq

file_path = '/Users/educifuentes/code/greenlab-censos/seeds/ine/personas_censo2024.parquet'

print(f"Reading file: {file_path}")
try:
    df = pd.read_parquet(file_path)
    print("Success with pandas!")
    print(df.head())
except Exception as e:
    print(f"Pandas failed: {e}")

try:
    table = pq.read_table(file_path)
    print("Success with pyarrow!")
except Exception as e:
    print(f"Pyarrow failed: {e}")
