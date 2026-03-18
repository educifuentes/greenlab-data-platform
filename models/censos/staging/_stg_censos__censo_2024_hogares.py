import pandas as pd
import os

from helpers.load_source_from_csv import load_source_dataframe

def stg_censos__censo_2024_hogares():
    """
    Loads hogares data using the path defined in the YAML configuration.
    """
    # Load the YAML file and extract DataFrame securely through the helper wrapper
    df = load_source_dataframe(
        table_name="hogares", 
        yaml_path="models/censos/sources/_src_censo_2024.yml"
    )

    # data types
    
    # cast all columns to nullable int32 (efficient for survey codes with missing values)
    df = df.apply(pd.to_numeric, errors='ignore')
    for col in df.select_dtypes(include=['number']).columns:
        df[col] = df[col].astype('Int32')

    # leave only 10,000 rows
    df = df.head(10000)
    
    return df
