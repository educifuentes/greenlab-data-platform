import pandas as pd

from models.contaminantes.staging._stg_contaminantes__energia_centrales_00_15 import stg_contaminantes__energia_centrales_00_15

from utilities.data_transformations.column_names_tosnakecase import to_snake_case
from utilities.data_transformations.cast_to_date import cast_column_to_date

def int_contaminantes__energia_centrales_00_15():
    df = stg_contaminantes__energia_centrales_00_15()

    # rename
    df = to_snake_case(df)

    # Cast 'fecha' to date. '1/2/14' is m/d/y, so we specify the format.
    df = cast_column_to_date(df, "fecha", date_format="%m/%d/%y")

    # data types
    # (fecha is already cast above)

    return df