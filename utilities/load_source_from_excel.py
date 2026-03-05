import pandas as pd
import openpyxl

from utilities.yaml_loader import load_yaml_config

def load_source_from_excel(table_name: str, yaml_path: str = "models/contaminantes/sources/_src_contaminantes.yml", nrows: int = None) -> pd.DataFrame:
    """
    Loads a source Excel file into a pandas DataFrame using the table name.
    It reads the YAML configuration to find the corresponding Excel path and worksheet name.
    Optionally pass nrows to limit how many rows are read from disk (much faster for large files).
    """
    config = load_yaml_config(yaml_path)
    sources = config.get("sources", [])
    
    excel_path = None
    sheet_name = None
    for source in sources:
        for table in source.get("tables", []):
            if table.get("name") == table_name:
                excel_path = table.get("path")
                sheet_name = table.get("worksheet")
                break
        if excel_path:
            break
            
    if not excel_path:
        raise ValueError(f"Table '{table_name}' not found in {yaml_path}")
        
    return pd.read_excel(excel_path, sheet_name=sheet_name, nrows=nrows)