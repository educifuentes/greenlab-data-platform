import pandas as pd
from utilities.yaml_loader import load_yaml_config

def load_source_dataframe(table_name: str, yaml_path: str = "models/contaminantes/sources/_src_contaminantes.yml") -> pd.DataFrame:
    """
    Loads a source CSV into a pandas DataFrame using the table name.
    It reads the YAML configuration to find the corresponding CSV path.
    """
    config = load_yaml_config(yaml_path)
    sources = config.get("sources", [])
    
    csv_path = None
    for source in sources:
        for table in source.get("tables", []):
            if table.get("name") == table_name:
                csv_path = table.get("path")
                break
        if csv_path:
            break
            
    if not csv_path:
        raise ValueError(f"Table '{table_name}' not found in {yaml_path}")
        
    return pd.read_csv(csv_path)