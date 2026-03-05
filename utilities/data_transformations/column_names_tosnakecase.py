import pandas as pd
import re

def to_snake_case(df: pd.DataFrame) -> pd.DataFrame:
    """
    Renames all columns in a pandas DataFrame to snake_case.
    
    Converts:
    - CamelCase to camel_case
    - Spaces, hyphens, and special characters to underscores
    - Lowercases everything
    - Removes consecutive, leading, and trailing underscores
    
    Aligns with PEP 8 style guide for Python variable names.
    """
    def clean_name(name):
        if not isinstance(name, str):
            name = str(name)
            
        # Insert underscore between lower case and upper case letters (for CamelCase)
        name = re.sub(r'(?<=[a-z0-9])([A-Z])', r'_\1', name)
        
        # Replace non-alphanumeric characters with underscores
        name = re.sub(r'[^a-zA-Z0-9]', '_', name)
        
        # Lowercase everything
        name = name.lower()
        
        # Remove multiple consecutive underscores
        name = re.sub(r'_+', '_', name)
        
        # Remove leading and trailing underscores
        name = name.strip('_')
        
        return name

    # Rename columns using the clean_name function
    df.columns = [clean_name(col) for col in df.columns]
    
    return df