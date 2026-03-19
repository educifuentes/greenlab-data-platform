# Capas de Arquitectura de Datos

## 1. Staging (Ingesta)
- **Objetivo**: Ingesta de datos sin procesar (raw).
- **Reglas**: Sin transformaciones. Representación 1:1 con los datos de origen.

## 2. Intermediate (Intermedia)
- **Objetivo**: Limpieza y normalización de datos.
- **Acciones**:
  - Renombrar columnas para mantener consistencia.
  - Asignar los tipos de datos correctos (casting).
  - Selección y ordenamiento de columnas.
  - Formatear cadenas de texto (strings) y eliminar valores atípicos (outliers).

## 3. Final
- **Objetivo**: Crear tablas de Hechos (Fact) y Dimensiones (Dimension).
- **Prefijos**: `_fct_<nombre>` o `_dim_<nombre>`.

## 4. Tablas BI
- **Objetivo**: Tablas finales unidas, optimizadas para herramientas de visualización y análisis (Tableau, Streamlit, etc.).
