# Data Pipeline

@[render_data_pipeline_chart]

### Capas

0. **Sources:** Data raw en variedad de formatos (excels, csv, json, bases de datos, APIs, etc.)
1. **Staging:** Cada fuente se asocia 1 a 1 a un modelo staging. Preparan la base cruda siendo los bloques de construcción más pequeños del proyecto.
2. **Intermediate:** Se aplican transformaciones, joins y otros. Generan componentes modulares reutilizables para no duplicar código en pasos futuros.
3. **Marts:** Datasets curados "fuente de verdad". Toman forma de Hechos (facts) o dimensiones (dim).
4. **Exposures:** Combinaciones de los mart models optimizadas para el consumo de herramientas de visualización y análisis (Tableau, R, etc.) (tablas agregadas o formato long wide segun mejor caso de uso)

### Tablas de hechos y dimensiones

**Fact tables**
Almacenan eventos de negocio cuantitativos y medibles (por ejemplo: ventas, clics, transacciones). Suelen ser largas y estrechas.

**Dimension tables**
Dan contexto descriptivo (por ejemplo: cliente, producto, ubicación). Suelen ser anchas, con diversos atributos de texto.

Nota: inspirado modelado de datos usado por [dbt](https://www.getdbt.com/blog/modular-data-modeling-techniques)
