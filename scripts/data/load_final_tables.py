"""
load_final_tables.py
---------------------
Loads all contaminantes energy data (no row limit), applies the same
transformations as _int_contaminantes__energia_centrales, and exports
the result to seeds/outputs/fct_emisiones_energia.parquet.

Run from the repo root:
    python scripts/data/load_final_tables.py
"""

import sys
import os

# Ensure repo root is on the path so all imports resolve
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import pandas as pd
from utilities.load_source_from_excel import load_source_from_excel
from utilities.data_transformations.column_names_tosnakecase import to_snake_case
from utilities.data_transformations.cast_to_date import cast_column_to_date, cast_spanish_month_col_to_date

OUTPUT_PATH = "seeds/outputs/fct_emisiones_energia.parquet"
OUTPUT_CSV_PATH = "seeds/outputs/fct_emisiones_energia.csv"

COLUMNS = [
    "nombre_central",
    "llave_nombre",
    "fuente_tipo",
    "fuente_subtipo",
    "region",
    "energia_tipo",
    "factor_ernc",
    "fecha",
    "hora_1",  "hora_2",  "hora_3",  "hora_4",  "hora_5",  "hora_6",
    "hora_7",  "hora_8",  "hora_9",  "hora_10", "hora_11", "hora_12",
    "hora_13", "hora_14", "hora_15", "hora_16", "hora_17", "hora_18",
    "hora_19", "hora_20", "hora_21", "hora_22", "hora_23", "hora_24",
]


def load_all():
    print("Loading source files (full data, no row limit)...")

    # --- 2000–2023: same structure, use to_snake_case ---
    df_00_15 = load_source_from_excel("Generacion de Energia por Central - 2000 a 2015")
    df_16_19 = load_source_from_excel("Generacion de Energia por Central - 2016 a 2019")
    df_20_22 = load_source_from_excel("Generacion de Energia por Central - 2020 a 2022")
    df_23    = load_source_from_excel("Generacion de Energia por Central - 2023")

    print(f"  2000–2015: {len(df_00_15):,} rows")
    print(f"  2016–2019: {len(df_16_19):,} rows")
    print(f"  2020–2022: {len(df_20_22):,} rows")
    print(f"  2023:      {len(df_23):,} rows")

    df_00_15 = to_snake_case(df_00_15)
    df_16_19 = to_snake_case(df_16_19)
    df_20_22 = to_snake_case(df_20_22)
    df_23    = to_snake_case(df_23)

    df = pd.concat([df_00_15, df_16_19, df_20_22, df_23], ignore_index=True)
    df = cast_column_to_date(df, "fecha", date_format="%m/%d/%y")
    df.rename(columns={
        "ernc_convencional": "energia_tipo",
        "tipo":              "fuente_tipo",
        "subtipo":           "fuente_subtipo",
    }, inplace=True)

    # --- 2024: different column names ---
    df_24 = load_source_from_excel("Generacion de Energia por Central - 2024")
    print(f"  2024:      {len(df_24):,} rows")

    df_24.rename(columns={
        "central_name":          "nombre_central",
        "ernc_factor":           "factor_ernc",
        "tipo_energia":          "energia_tipo",
        "tipo_fuente":           "fuente_tipo",
        "subtipo_fuente":        "fuente_subtipo",
        "_ops_por_hora_new.fecha": "fecha",
    }, inplace=True)
    df_24 = df_24.rename(columns={str(i): f"hora_{i}" for i in range(1, 26)})
    df_24 = cast_spanish_month_col_to_date(df_24, "fecha", year=2024)

    # --- Select final columns & union ---
    df    = df[COLUMNS]
    df_24 = df_24[COLUMNS]
    result = pd.concat([df, df_24], ignore_index=True)

    print(f"\nTotal rows: {len(result):,}")
    return result


def main():
    df = load_all()

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_parquet(OUTPUT_PATH, index=False)
    print(f"\nSaved → {OUTPUT_PATH}")
    df.to_csv(OUTPUT_CSV_PATH, index=False)
    print(f"Saved → {OUTPUT_CSV_PATH}")


if __name__ == "__main__":
    main()