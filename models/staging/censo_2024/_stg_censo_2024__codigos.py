import pandas as pd
import os

from utilities.yaml_loader import load_yaml_config

def _get_table_path(table_name):
    config = load_yaml_config('models/staging/_src_censo_2024__codigos.yml')
    # The yaml structure is: {'tables': [{'name': ..., 'path': ...}, ...]}
    tables = config['tables']
    rel_path = next(t['path'] for t in tables if t['name'] == table_name)
    
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
    return os.path.join(project_root, rel_path)

def _read_csv(file_path):
    # Latin1 is common for Chilean government data (contains accents like á, é, ñ)
    return pd.read_csv(file_path, sep=',', encoding='latin1')

def stg_censo_2024__codigos_regiones():
    file_path = _get_table_path('regiones')
    df =_read_csv(file_path)

    df.rename(columns={'region_cod': 'cod_region'}, inplace=True)
    return df

def stg_censo_2024__codigos_provincias():
    file_path = _get_table_path('provincias')
    df =_read_csv(file_path)

    df.rename(columns={'Cod_provincia': 'cod_provincia', 'Provincia': 'provincia_nombre'}, inplace=True)
    return df

def stg_censo_2024__codigos_comunas():
    file_path = _get_table_path('comunas')
    df =_read_csv(file_path)

    return df
