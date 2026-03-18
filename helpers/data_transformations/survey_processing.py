import pandas as pd
import json
import os

def map_survey_codes(df: pd.DataFrame, mapping_path: str) -> pd.DataFrame:
    """
    Maps survey codes in a dataframe to their corresponding text values based on a JSON mapping file.
    Converts mapped columns to categorical dtype.

    Args:
        df (pd.DataFrame): The dataframe containing survey data.
        mapping_path (str): Path to the JSON file containing the mapping. 
                            Can be absolute or relative to the project root.

    Returns:
        pd.DataFrame: The dataframe with mapped values and categorical columns.
    """
    # Resolve mapping path relative to project root if it's not absolute
    if not os.path.isabs(mapping_path):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        mapping_path = os.path.join(project_root, mapping_path)

    if not os.path.exists(mapping_path):
        raise FileNotFoundError(f"Mapping file not found at: {mapping_path}")

    with open(mapping_path, 'r', encoding='utf-8') as f:
        mapping = json.load(f)

    # Copy df to avoid setting on copy warning if a slice was passed
    df = df.copy()

    for col, codes in mapping.items():
        if col in df.columns:
            # Ensure column is treated as object/string for mapping to work if keys in json are strings
            # But keys in JSON are always strings. If df has ints, we need to handle that.
            # Best practice: convert column to string temporarily for mapping, or convert keys to match col type?
            # Given typically survey codes are integers but can be 'NA', '99', etc, mixed types happen.
            # Safe bet: Convert series to string, map, then categorical.
            
            # Helper to handle potential mixed types in source or map keys
            # The mapping keys in the provided JSON are strings ("1", "2", ...)
            
            # Convert column to string to ensure matching with JSON keys
            df[col] = df[col].astype(str)
            
            # Map values
            # Using map alone might produce NaNs for unmapped values if we don't pass a fallback.
            # simpler approach: use replace. But replace might be slow on large DFs.
            # map is faster. Let's use map and fillna with original if needed, but here we want to map.
            # If a value is NOT in the map, it should probably stay as is or become NaN?
            # Usually we want to keep it if it's not a code, but typically all valid codes are mapped.
            
            # Let's use replace for safety on partial matches (though map is better for full col transformation)
            # Actually, let's look at the requirement: "map th evalues of the df to the adhoc values"
            
            df[col] = df[col].map(codes).fillna(df[col])
            
            # Convert to category
            df[col] = df[col].astype('category')

    return df

def map_survey_personas(df: pd.DataFrame, mapping_path: str) -> pd.DataFrame:
    """
    Maps survey codes in the personas dataframe to their corresponding text values based on a JSON mapping file.
    Includes specific logic for scale groupings and special numeric range handling.

    Args:
        df (pd.DataFrame): The personas dataframe containing survey data.
        mapping_path (str): Path to the JSON file containing the mapping. 

    Returns:
        pd.DataFrame: The dataframe with mapped values and categorical columns.
    """
    # Resolve mapping path relative to project root if it's not absolute
    if not os.path.isabs(mapping_path):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        mapping_path = os.path.join(project_root, mapping_path)

    if not os.path.exists(mapping_path):
        raise FileNotFoundError(f"Mapping file not found at: {mapping_path}")

    with open(mapping_path, 'r', encoding='utf-8') as f:
        mapping_data = json.load(f)

    escalas_comunes = mapping_data.get('escalas_comunes', {})
    mapeo_variables = mapping_data.get('mapeo_variables', {})

    # Copy df to avoid setting on copy warning
    df = df.copy()

    # Si/No/NR/NA scale for p15* columns
    si_no_scale = escalas_comunes.get('si_no_nr_na', {})
    
    # Difficulty scale for p32a through p32f
    difficulty_scale = escalas_comunes.get('dificultad_salud', {})

    # Iterate through columns to apply mapping
    for col in df.columns:
        codes = None
        
        # 1. Check for specific prefix logic
        if col.startswith('p15'):
            codes = si_no_scale
        elif col.startswith('p32') and len(col) >= 4 and col[3] in ['a', 'b', 'c', 'd', 'e', 'f']:
             # Matches p32a, p32b, ..., p32f and potential suffixes
            codes = difficulty_scale
        
        # 2. Check for explicit mapping in mapeo_variables
        elif col in mapeo_variables:
            codes = mapeo_variables[col]
            
            # Special handling for p48_anio_nac_uh
            if col == 'p48_anio_nac_uh':
                # Convert to numeric, forcing errors to NaNs
                # But wait, original values might be ints.
                # If value is between 1934 and 2024, keep it.
                # Otherwise map it using codes (likely '99' -> No responde)
                
                # Logic:
                # 1. Convert to numeric to check range.
                # 2. If valid year, keep as string of year.
                # 3. If not valid year (e.g. 99), map it.
                
                # To do this vectorially:
                # Convert col to numeric, coaxing errors
                numeric_series = pd.to_numeric(df[col], errors='coerce')
                
                # Identify valid years
                valid_years = (numeric_series >= 1934) & (numeric_series <= 2024)
                
                # Create a temporary series for mapping
                # Convert original to string for mapping lookup
                str_series = df[col].astype(str)
                mapped_values = str_series.map(codes)
                
                # Combine: where valid year, use original numeric (as str); else use mapped value
                # Note: if mapping fails (NaN), fill with original value? Or leave as NaN?
                # The prompt says "otherwise, map it to 'No response' or 'NA' as per the JSON."
                # So if it's 99, it should map. If it's something else not in map and not in range? 
                # Preserving original seems safest default if not mapped.
                
                final_values = str_series.where(valid_years, mapped_values.fillna(str_series))
                
                df[col] = final_values.astype('category')
                continue # Skip standard mapping logic for this column

        if codes:
            # Standard mapping logic
            
            # Convert column to string to ensure matching with JSON keys
            df[col] = df[col].astype(str)
            
            # Map values
            # Using map and fillna with original values for those not found in mapping
            df[col] = df[col].map(codes).fillna(df[col])
            
            # Convert to category
            df[col] = df[col].astype('category')

    return df
