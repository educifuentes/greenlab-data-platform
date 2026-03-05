import pandas as pd

from models.staging.censo_2024._stg_censo_2024__hogares import stg_censo_2024__hogares
from models.staging.censo_2024._stg_censo_2024__codigos import stg_censo_2024__codigos_regiones, stg_censo_2024__codigos_provincias, stg_censo_2024__codigos_comunas

from utilities.data_transformations.survey_processing import map_survey_codes
from utilities.yaml_loader import get_table_config

def int_censo_2024__hogares():
    df = stg_censo_2024__hogares()

    # replace survey codes with categorical values
    table_config = get_table_config('censos', 'hogares', 'models/staging/censo_2024/_src_censo_2024.yml')
    mapping_path = table_config.get('survey_dictionary_path')
    df = map_survey_codes(df, mapping_path)

    # join with geo code tables
    df = pd.merge(df, stg_censo_2024__codigos_regiones(), left_on='region', right_on='cod_region', how='left')
    df = pd.merge(df, stg_censo_2024__codigos_provincias(), left_on='provincia', right_on='cod_provincia', how='left')
    df = pd.merge(df, stg_censo_2024__codigos_comunas(), left_on='comuna', right_on='cod_comuna', how='left')

    # drop the original columns
    df.drop(columns=['region', 'provincia', 'comuna'], inplace=True)

    # reorder columns
    leading_cols = ['id_hogar', 'region_nombre', 'provincia_nombre', 'comuna_nombre']
    # Only include existing columns to be safe
    leading_cols = [c for c in leading_cols if c in df.columns]
    other_cols = [c for c in df.columns if c not in leading_cols]
    
    df = df[leading_cols + other_cols]

    return df
