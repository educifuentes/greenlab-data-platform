import pandas as pd
from helpers.utilities.yaml_loader import load_yaml_config

def load_source(table_name: str, yaml_path: str = "models/generacion_electrica/sources/_src_generacion_electrica.yml", format: str = "csv", **kwargs) -> pd.DataFrame:
    """
    Loads a source file into a pandas DataFrame using the table name.
    It reads the YAML configuration to find the corresponding file path.
    Supports 'csv' (default), 'excel', and will auto-detect '.parquet' files.
    """
    config = load_yaml_config(yaml_path)
    sources_dict_or_list = config.get("sources", [])
    
    # Support both list of sources and dict of sources (e.g. keyed by schema)
    if isinstance(sources_dict_or_list, dict):
        sources = sources_dict_or_list.values()
    else:
        sources = sources_dict_or_list
        
    file_path = None
    sheet_name = None
    for source in sources:
        for table in source.get("tables", []):
            if table.get("name") == table_name:
                file_path = table.get("path")
                sheet_name = table.get("worksheet")
                break
        if file_path:
            break
            
    if not file_path:
        raise ValueError(f"Table '{table_name}' not found in {yaml_path}")
        
    if format == "excel":
        if 'nrows' in kwargs and kwargs['nrows'] is not None:
            return pd.read_excel(file_path, sheet_name=sheet_name, nrows=kwargs['nrows'])
        return pd.read_excel(file_path, sheet_name=sheet_name, **kwargs)
        
    if file_path.endswith(".parquet"):
        return pd.read_parquet(file_path, **kwargs)
        
    return pd.read_csv(file_path, **kwargs)
