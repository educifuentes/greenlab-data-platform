# Data Pipeline

Data se desarrolla en 4 capas, cada una con su propósito definido.

## Modelado en Capas

Modulariza el desarollo de datos en diferentes fases lógicas para simplificar la estructura del proyecto.

### Layers:

0. **Sources:** Se definen los orígenes en `sources.yml`, representando los datos crudos del data warehouse.
1. **Staging:** Cada fuente se asocia 1 a 1 a un modelo staging. Preparan la base cruda siendo los bloques de construcción más pequeños del proyecto.
2. **Intermediate:** Se aplican transformaciones, joins y lógica de negocio. Generan componentes modulares reutilizables para no duplicar código en pasos futuros.
3. **Marts:** Modelos finales, se combinan modelos anteriores para llegar a tablas curadas de Hechos (facts) o dimensiones (dim).
4. **Exposures:** Tablas optimizadas para ser consumidas por herramientas de visualización y análisis (Tableau, R, PowerBI, etc.).
