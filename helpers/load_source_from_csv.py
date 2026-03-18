import pandas as pd

from helpers.yaml_loader import load_yaml_config

def load_source_dataframe(table_name: str, yaml_path: str = "models/generacion_electrica/sources/_src_generacion_electrica.yml") -> pd.DataFrame:
    """
    Loads a source CSV into a pandas DataFrame using the table name.
    It reads the YAML configuration to find the corresponding CSV path.
    """
    config = load_yaml_config(yaml_path)
    sources_dict_or_list = config.get("sources", [])
    
    # If sources is a dict (e.g. keyed by schema), iterate over its values
    if isinstance(sources_dict_or_list, dict):
        sources = sources_dict_or_list.values()
    else:
        sources = sources_dict_or_list
        
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
        
    if csv_path.endswith(".parquet"):
        return pd.read_parquet(csv_path)
    return pd.read_csv(csv_path)