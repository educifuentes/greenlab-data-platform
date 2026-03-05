import pandas as pd

def cast_column_to_date(df: pd.DataFrame, column_name: str, date_format: str = None, dayfirst: bool = False, as_datetime: bool = False) -> pd.DataFrame:
    """
    Casts a specified column in a pandas DataFrame to datetime format.
    
    Args:
        df: The pandas DataFrame.
        column_name: The name of the column to cast.
        date_format: Optional specific date format string (e.g., '%m/%d/%y').
                     If provided, pandas will use it to parse the dates.
        dayfirst: Boolean flag indicating if the day is the first element in the date format
                  when the date format is ambiguous. Defaults to False (which implies month first,
                  common in some Latin American data sources for m/d/y formats like '1/2/14').
        as_datetime: If True, returns column as pandas datetime64, otherwise returns Python date objects. Defaults to False.
                  
    Returns:
        The DataFrame with the specified column cast to datetime.
    """
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in the DataFrame.")
        
    df[column_name] = pd.to_datetime(df[column_name], format=date_format, dayfirst=dayfirst, errors='coerce')
    if not as_datetime:
        df[column_name] = df[column_name].dt.date
    
    return df
