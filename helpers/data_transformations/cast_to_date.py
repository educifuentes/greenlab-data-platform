import pandas as pd
from datetime import date

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


# Spanish abbreviated month name → numeric month
_SPANISH_MONTHS = {
    "ene": "01", "feb": "02", "mar": "03", "abr": "04",
    "may": "05", "jun": "06", "jul": "07", "ago": "08",
    "sep": "09", "oct": "10", "nov": "11", "dic": "12",
}

def cast_spanish_month_col_to_date(df: pd.DataFrame, column_name: str, year: int = 2024) -> pd.DataFrame:
    """
    Parses a column whose values contain Spanish abbreviated month names
    (e.g. "ene 01", "dic 31") and converts it to a Python date.
    The year for every row is forced to `year` (default 2024).

    Args:
        df: The pandas DataFrame.
        column_name: The column to parse.
        year: The year to assign to every parsed date. Defaults to 2024.

    Returns:
        The DataFrame with the column replaced by Python date objects.
    """
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in the DataFrame.")

    def _parse(value):
        if pd.isna(value):
            return None
        s = str(value).strip().lower()
        for esp, num in _SPANISH_MONTHS.items():
            s = s.replace(esp, num)
        # After substitution the format is always DD-MM (e.g. "01-01" from "01-ene")
        parsed = pd.to_datetime(s, format="%d-%m", errors="coerce")
        if pd.isna(parsed):
            return None
        return date(year, parsed.month, parsed.day)

    df[column_name] = df[column_name].apply(_parse)
    return df
