# Data Architecture Layers

## 1. Staging
- **Goal**: Raw data ingestion.
- **Rules**: No transformations. 1:1 representation with the source data.

## 2. Intermediate
- **Goal**: Data cleaning and normalization.
- **Actions**:
  - Rename columns for consistency.
  - Cast correct data types.
  - Column selection and ordering.
  - Format strings and remove outliers.

## 3. Final
- **Goal**: Create Fact and Dimension tables.
- **Prefixes**: `_fct_<name>` or `_dim_<name>`.

## 4. BI Tables
- **Goal**: Final joined tables optimized for visualization and analysis tools (Tableau, Streamlit, etc.).
