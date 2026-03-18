import pandas as pd
import os

from helpers.yaml_loader import load_yaml_config

def stg_censos__censo_2024_personas():
    """
    Loads personas data using the path defined in the YAML configuration.
    """
    # Load the YAML file as a dictionary
    config = load_yaml_config('models/censos/sources/_src_censo_2024.yml')
    
    # Extract the path for the 'personas' table
    tables = config['sources']['censos']['tables']
    rel_path = next(t['path_sample'] for t in tables if t['name'] == 'personas')
    
    # Construct the absolute path (project root is 3 levels up from this staging file)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
    file_path = os.path.join(project_root, rel_path)

    # read parquet
    df = pd.read_csv(file_path, delimiter=';', encoding='latin1')

    # data types
    
    # cast all columns to nullable int32 (efficient for survey codes with missing values)
    df = df.apply(pd.to_numeric, errors='ignore')
    for col in df.select_dtypes(include=['number']).columns:
        df[col] = df[col].astype('Int32')

    # leave only 10,000 rows
    df = df.head(10_000)
    
    return df
