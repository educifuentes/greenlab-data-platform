# Capas de Arquitectura de Datos

## 1. Staging

- **Objetivo**: Ingesta de datos sin procesar (raw).
- **Reglas**: Sin transformaciones. Representación 1:1 con los datos de origen.
- Ejemplos:
  - `stg_daily_sales_by_product`
  - `stg_product`

## 2. Intermediate

- **Objetivo**: Limpieza y normalización de datos. Aqui ocurren la mayoria de las transformaciones, join y limpieza.
- **Acciones**:
  - Renombrar columnas para mantener consistencia.
  - Asignar los tipos de datos correctos (casting).
  - Selección y ordenamiento de columnas.
  - Formatear de strings
- Ejemplos:
  - `int_daily_sales_by_product`

## 3. Marts

- **Objetivo**: Combinar tablas anteriores para lograr tablas de Hechos (Fact) y Dimensiones (Dimension). Esta es data "cuarada" lista para ser consumida y combinar para generar los modelos a consumirse por Tableau u otras herramientas de visualización.
- **Prefijos**: `_fct_<nombre>` o `_dim_<nombre>`.
- Ejemplos:
  - `fct_daily_sales_by_product`
  - `dim_product`

## 4. Exposures

- **Objetivo**: Tablas finales unidas, optimizadas para herramientas de visualización y análisis (Tableau, Streamlit, etc.).
  Ejemplos
- `exp_daily_sales_by_product`
- `exp_monthly_sales_by_product`
