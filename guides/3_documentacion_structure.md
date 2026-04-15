# Documentación

Esta guía explica cómo documentar correctamente las distintas capas de datos del proyecto: fuentes (sources), modelos (marts/intermediates/staging) y métricas. Toda la documentación se maneja a través de archivos YAML ubicados junto a los scripts o en su carpeta de esquema correspondiente.

### Sources

Para documentar las fuentes de datos externas, se crea un archivo `_src_<esquema>.yml` en la carpeta correspondiente dentro de `models/sources/`. Este archivo lista la descripción general de la fuente, su origen (URL si aplica) y las tablas o archivos específicos de donde se lee.

**Ejemplo:** `models/sources/geografia/_src_geografia.yml`

```yaml
sources:
  - name: geografia
    description: "Archivo Codigos MAESTROS de Comunas/Provincias/Regiones. Descripcion todos los codigos de unidades geograficas de Chile de censos, casen, etc"
    url: https://docs.google.com/spreadsheets/d/1hHXUhAbdMPKTNxaHNbzeBlHIlSsgzAXlc4u_r48V62Y/edit#gid=695826548
    tables:
      - name: codigos_comuna
        path: seeds/geografia/cod_comuna.csv
      - name: codigos_provincia
        path: seeds/geografia/cod_provincia.csv
      - name: codigos_region
        path: seeds/geografia/cod_region.csv
      - name: codigos_pais
        path: seeds/geografia/cod_pais.csv
```

### Models

Los modelos (tablas derivadas, ya sean staging, intermediates o marts) se documentan con un archivo `.yml` que debe llevar exactamente el mismo nombre que el script de Python, pero con extensión `.yml`. Este archivo documenta tanto la descripción general del modelo como el diccionario de datos (columnas).

**Ejemplo:** `models/marts/termoelectricas/_fct_termoelectricas__emisiones.yml`

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
      - name: dia
        description: "Fecha (agregación diaria)."
      # ... Puedes agregar cuantas columnas sean necesarias en este formato ...
```

### Metrics

Las métricas del negocio se definen por esquema en un archivo `<esquema>_metrics.yml` directamente dentro de la carpeta `models/metrics/`. Las métricas se definen como una lista plana, especificando a qué grupo pertenecen, fórmulas de cálculo, unidades y descripción para alimentar la interfaz de documentación.

**Ejemplo:** `models/metrics/termoelectricas_metrics.yml`

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
