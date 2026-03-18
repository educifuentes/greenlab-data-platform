import pandas as pd

from models.censos.staging._stg_censos__censo_2024_personas import stg_censos__censo_2024_personas
from models.censos.staging._stg_censos__censo_2024_codigos import stg_censos__censo_2024_codigos_regiones, stg_censos__censo_2024_codigos_provincias, stg_censos__censo_2024_codigos_comunas

from helpers.data_transformations.survey_processing import map_survey_personas
from helpers.yaml_loader import get_table_config

def int_censos__censo_2024_personas():
    personas_df = stg_censos__censo_2024_personas()

    # replace survey codes with categorical values
    table_config = get_table_config('censos', 'personas', 'models/censos/sources/_src_censo_2024.yml')
    mapping_path = table_config.get('survey_dictionary_path')
    personas_df = map_survey_personas(personas_df, mapping_path)

    # join with geo code tables
    personas_df = pd.merge(personas_df, stg_censos__censo_2024_codigos_regiones(), left_on='region', right_on='cod_region', how='left')
    personas_df = pd.merge(personas_df, stg_censos__censo_2024_codigos_provincias(), left_on='provincia', right_on='cod_provincia', how='left')
    personas_df = pd.merge(personas_df, stg_censos__censo_2024_codigos_comunas(), left_on='comuna', right_on='cod_comuna', how='left')

    # drop the original columns
    personas_df.drop(columns=['region', 'provincia', 'comuna'], inplace=True)

    # reorder columns
    leading_cols = ['id_persona', 'region_nombre', 'provincia_nombre', 'comuna_nombre']
    # Only include existing columns to be safe
    leading_cols = [c for c in leading_cols if c in personas_df.columns]
    other_cols = [c for c in personas_df.columns if c not in leading_cols]
    
    personas_df = personas_df[leading_cols + other_cols]

    return personas_df
