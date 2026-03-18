Build a function that scnas the tree of models folder, and based on that, build a df with the following columns:

schema
stage
model

To pouplate it, grab the names of the oy files and follow

_<stage>_<schema>\_\_<model>

omith the **pycache** subdirectories

example

for

models/generacion_electrica

├── docs
├── finals
│ ├── **init**.py
│ ├── **pycache**
│ │ ├── **init**.cpython-314.pyc
│ │ └── \_fct_generacion_electrica.cpython-314.pyc
│ └── \_fct_generacion_electrica.py
├── intermediate
│ ├── **pycache**
│ │ └── \_int_generacion_electrica**energia_centrales.cpython-314.pyc
│ └── \_int_generacion_electrica**energia_centrales.py
├── metrics
│ └── **init**.py
├── sources
│ └── \_src_generacion_electrica.yml
└── staging
├── **init**.py
├── **pycache**
│ ├── **init**.cpython-314.pyc
│ ├── \_stg_generacion_electrica**energia_centrales_00_15.cpython-314.pyc
│ ├── \_stg_generacion_electrica**energia_centrales_16_19.cpython-314.pyc
│ ├── \_stg_generacion_electrica**energia_centrales_20_22.cpython-314.pyc
│ ├── \_stg_generacion_electrica**energia_centrales_23.cpython-314.pyc
│ └── \_stg_generacion_electrica**energia_centrales_24.cpython-314.pyc
├── \_stg_generacion_electrica**energia_centrales_00_15.py
├── \_stg_generacion_electrica**energia_centrales_16_19.py
├── \_stg_generacion_electrica**energia_centrales_20_22.py
├── \_stg_generacion_electrica**energia_centrales_23.py
└── \_stg_generacion_electrica**energia_centrales_24.py

    expected df:

    schema | stage | model
    generacion_electrica | staging | _stg_generacion_electrica__energia_centrales_00_15
    generacion_electrica | staging | _stg_generacion_electrica__energia_centrales_16_19
    generacion_electrica | staging | _stg_generacion_electrica__energia_centrales_20_22
    generacion_electrica | staging | _stg_generacion_electrica__energia_centrales_23
    generacion_electrica | staging | _stg_generacion_electrica__energia_centrales_24
    generacion_electrica | intermediate | _int_generacion_electrica__energia_centrales
    generacion_electrica | final | _fct_generacion_electrica
    generacion_electrica | exposure | exp_generacion_electrica_by_month
