# Greenlab Data Platform

Base de conocimiento y plataforma unificada de datos para los proyectos de Greenlab.

## Características (Features)

Esta plataforma centraliza los procesos de datos y los documenta mediante una interfaz web ágil y moderna. Entre sus características principales destacan:

- **Catálogo de Modelos:** Buscador y repositorio interactivo para explorar modelos de datos (organizados por etapas y esquemas de negocio).
- **Documentación Dinámica:** Generación automática de diccionarios de datos para tablas y métricas, consumiendo directamente la metadata de archivos `.yml`.
- **Linaje de Datos Integrado:** Visualización gráfica (mediante diagramas Mermaid generados automáticamente) del trazado de dependencias entre modelos, desde las fuentes hasta los _marts_.
- **Guías de Uso y Mejores Prácticas:** Sección dedicada a la documentación técnica interna (flujos en Git, modelado en base de datos, convención de nombres y despliegues).

## Mantenimiento y Releases

Para registrar y generar nuevas versiones (_releases_) de la plataforma, ejecuta el script automatizado mediante terminal:

```bash
./scripts/release.sh
```
