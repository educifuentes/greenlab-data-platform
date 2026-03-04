import pandas as pd
import os

from utilities.yaml_loader import load_yaml_config

def stg_censo_2024__viviendas():
    """
    Loads viviendas data using the path defined in the YAML configuration.
    """
    # Load the YAML file as a dictionary
    config = load_yaml_config('models/staging/censo_2024/_src_censo_2024.yml')
    
    # Extract the path for the 'viviendas' table
    tables = config['sources']['censos']['tables']
    rel_path = next(t['path'] for t in tables if t['name'] == 'viviendas')
    
    # Construct the absolute path (project root is 3 levels up from this staging file)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
    file_path = os.path.join(project_root, rel_path)

    # Read the parquet file
    df = pd.read_parquet(file_path)

    # leave only 100,000 rows   
    df = df.head(100000)
    
    return df
