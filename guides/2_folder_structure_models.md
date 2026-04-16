# Estructura de Carpetas y Archivos

Estrcutura de carpetas para los modelos:

```text
models/
├── sources/          # YAMLs que definen donde residen los datos.
├── staging/          # 1 a 1 con una fuente
├── intermediate/     # Uniones y agregaciones complejas que aún no son un hecho o dimensión.
├── marts/            # Tablas listas para el negocio (lógica de hechos y dimensiones).
├── metrics/          # Definiciones de métricas, KPIs y cálculos.
└── exposures/        # Capa final que sirve directamente a una herramienta de BI (ej. Tableau)
```

# Convenciones de Nombres

## Modelos

Formato: `_<capa>_<schema>__<nombre_tabla>.py`

i.e. `_stg_generacion_electrica__energia_centrales_00_15.py`
