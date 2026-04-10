# Data Pipeline

Data se desarrolla en 4 capas, cada una con su propósito definido.

![Data Pipeline](assets/images/model_layers.jpeg)

## Concepto: Modelado en Capas

El modelado en capas (inspirado en la arquitectura Medallion) divide los modelos de datos en diferentes fases lógicas para simplificar la estructura del proyecto. El objetivo es proporcionar un marco de trabajo fácil de mantener y escalar, permitiendo a los equipos enfocarse en el valor de negocio.

*Nota: Separar la data en capas es una convención de desarrollo, no un reemplazo para el diseño o modelado dimensional.*

### Pasos Clave del Enfoque:
0. **Fuentes (Layer Zero):** Se definen los orígenes en `sources.yml`, representando los datos crudos del data warehouse.
1. **Staging:** Cada fuente se asocia 1 a 1 a un modelo staging. Preparan la base cruda siendo los bloques de construcción más pequeños del proyecto.
2. **Intermediate:** Se aplican transformaciones, joins y lógica de negocio. Generan componentes modulares reutilizables para no duplicar código en pasos futuros.
3. **Marts:** Modelos finales, listos para usuarios de negocio y herramientas BI. Tablas anchas con un nivel de madurez analítico (ej: usuarios, órdenes).
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
