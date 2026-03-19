import os
import pandas as pd

def compress_csv(filepath):
    """
    Reads the file as binary lines to avoid encoding/separator issues.
    Keeps a maximum of 301 lines (header + 300 rows).
    """
    with open(filepath, 'rb') as f:
        lines = []
        for i, line in enumerate(f):
            if i > 300:  # line 0 is the header, lines 1-300 are data
                break
            lines.append(line)
            
    # Write the lines back to the file
    with open(filepath, 'wb') as f:
        for line in lines:
            f.write(line)

def compress_excel(filepath):
    dfs = pd.read_excel(filepath, sheet_name=None)
    modified = False
    for sheet_name, df in dfs.items():
        if len(df) > 300:
            dfs[sheet_name] = df.head(300)
            modified = True
            
    if modified:
        with pd.ExcelWriter(filepath) as writer:
            for sheet_name, df in dfs.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)

def compress_parquet(filepath):
    df = pd.read_parquet(filepath)
    if len(df) > 300:
        df = df.head(300)
        df.to_parquet(filepath, index=False)

def main():
    seeds_dir = "seeds"
    if not os.path.exists(seeds_dir):
        print(f"Directory '{seeds_dir}' not found.")
        return
        
    for root, dirs, files in os.walk(seeds_dir):
        for file in files:
            filepath = os.path.join(root, file)
            ext = os.path.splitext(filepath)[1].lower()
            
            try:
                if ext == '.csv':
                    compress_csv(filepath)
                    print(f"Processed CSV: {filepath}")
                elif ext in ['.xlsx', '.xls']:
                    compress_excel(filepath)
                    print(f"Processed Excel: {filepath}")
                elif ext == '.parquet':
                    compress_parquet(filepath)
                    print(f"Processed Parquet: {filepath}")
            except Exception as e:
                print(f"Failed to process {filepath}: {e}")

if __name__ == "__main__":
    main()
