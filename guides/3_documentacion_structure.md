# Documentación

### Sources

**Ejemplo:** `models/sources/geografia/_src_geografia.yml`

```yaml
sources:
  - name: geografia
    description: "Codigos maestros de comunas, provincias y regiones. Todos los codigos de unidades geograficas de Chile de censos, casen, etc"
    url: https://docs.google.com/spreadsheets/d/1hHXUhAbdMPKTNxaHNbzeBlHIlSsgzAXlc4u_r48V62Y/edit#gid=695826548
    tables:
      - name: codigos_comuna
        path: seeds/geografia/cod_comuna.csv
      - name: codigos_provincia
        path: seeds/geografia/cod_provincia.csv
      ...

```

### Models

```yaml
models:
  - name: _fct_termoelectricas__emisiones
    description: "Tabla mart que contiene información de emisiones diarias de centrales termoeléctricas."
    columns:
      - name: nombre_central
        description: "Nombre de la central termoeléctrica."
      - name: chimenea
        description: "Nombre de la chimenea asociada a la UGE."
      - name: uge
        description: "Unidad Generadora Eléctrica."
      # ... Puedes agregar cuantas columnas sean necesarias en este formato ...
```

### Metrics

```yaml
metrics:
  - name: "Emisiones CO2 Totales"
    group_name: "Emisiones Termoeléctricas"
    description: "Suma total de emisiones de Dióxido de Carbono en el periodo evaluado."
    calculation: "Suma de emisiones_co2_toneladas"
    unidad: "toneladas"

  - name: "Emisiones MP Totales"
    group_name: "Emisiones Termoeléctricas"
    description: "Suma total de Material Particulado emitido en el periodo evaluado."
    calculation: "Suma de emisiones_mp_toneladas"
    unidad: "toneladas"
```
