import pandas as pd

from models.generacion_electrica.staging._stg_generacion_electrica__energia_centrales_00_15 import stg_generacion_electrica__energia_centrales_00_15
from models.generacion_electrica.staging._stg_generacion_electrica__energia_centrales_16_19 import stg_generacion_electrica__energia_centrales_16_19
from models.generacion_electrica.staging._stg_generacion_electrica__energia_centrales_20_22 import stg_generacion_electrica__energia_centrales_20_22
from models.generacion_electrica.staging._stg_generacion_electrica__energia_centrales_23 import stg_generacion_electrica__energia_centrales_23
from models.generacion_electrica.staging._stg_generacion_electrica__energia_centrales_24 import stg_generacion_electrica__energia_centrales_24

from utilities.data_transformations.column_names_tosnakecase import to_snake_case
from utilities.data_transformations.cast_to_date import cast_column_to_date, cast_spanish_month_col_to_date

def int_generacion_electrica__energia_centrales():

    # load all periods
    df_00_15 = stg_generacion_electrica__energia_centrales_00_15()
    df_16_19 = stg_generacion_electrica__energia_centrales_16_19()
    df_20_22 = stg_generacion_electrica__energia_centrales_20_22()
    df_23 = stg_generacion_electrica__energia_centrales_23()
    df_24 = stg_generacion_electrica__energia_centrales_24()

    # tablas similares: 2000 al 2023
    df_00_15 = to_snake_case(df_00_15)
    df_16_19 = to_snake_case(df_16_19)
    df_20_22 = to_snake_case(df_20_22)
    df_23 = to_snake_case(df_23)
    df = pd.concat([df_00_15, df_16_19, df_20_22, df_23])
    # cast date
    df = cast_column_to_date(df, "fecha", date_format="%m/%d/%y")

    df.rename(columns={
        "ernc_convencional": "energia_tipo",
        "tipo": "fuente_tipo",
        "subtipo": "fuente_subtipo",
    }, inplace=True)



    # cambios puntuales en 2024
    df_24.rename(columns={
        "central_name": "nombre_central",
        "ernc_factor": "factor_ernc",
        "tipo_energia": "energia_tipo",
        "tipo_fuente": "fuente_tipo",
        "subtipo_fuente": "fuente_subtipo",
        '_ops_por_hora_new.fecha': "fecha",
    }, inplace=True)

    # horas renaming
    df_24 = df_24.rename(columns={str(i): f"hora_{i}" for i in range(1, 26)})

    # fecha
    df_24 = cast_spanish_month_col_to_date(df_24, "fecha", year=2024)

    # final union

    columns = [
        "nombre_central",
        "llave_nombre",
        "fuente_tipo",
        "fuente_subtipo",
        "region",
        "energia_tipo",
        "factor_ernc",
        "fecha",
        # horas
        "hora_1",
        "hora_2",
        "hora_3",
        "hora_4",
        "hora_5",
        "hora_6",
        "hora_7",
        "hora_8",
        "hora_9",
        "hora_10",
        "hora_11",
        "hora_12",
        "hora_13",
        "hora_14",
        "hora_15",
        "hora_16",
        "hora_17",
        "hora_18",
        "hora_19",
        "hora_20",
        "hora_21",
        "hora_22",
        "hora_23",
        "hora_24"
    ]

    df = df[columns]
    df_24 = df_24[columns]

    df = pd.concat([df, df_24])

    return df