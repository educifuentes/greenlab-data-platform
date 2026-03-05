# Pasos que hacer en cada Layer

## 1 Staging

- only loads data raw: no transformations
- it has to be a 1:1 represenation with the source

## 2 Intermediate

- rename columns
- cast correct data types
- make subselection of columns and set order
- data cleaning of values : format strings
- remove outliers, etc

### 3 Finals

create fact and dimensions tables, mixing the intermediate tables

prefix are _fct_<<fact*name>> or \_dim*<entity_name>

### 4 BI Tables

Mixes facts and dimension tables for a specific analysis or visualization

- tables ready to use for a analysys or visualization tool such as Tablea, R, PowerBI, etc
