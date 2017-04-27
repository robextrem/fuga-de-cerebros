# Fuga de Cerebros

El proyecto Fuga de Cerebros surge como una propuesta para la generación de conexiones entre entre becarios y ex becarios de CONACyT que se encuentran en el extranjero; y empresas e instituciones mexicanas generadoras de proyectos que demandan profesionales altamente calificados.

Nuestro trabajo consiste en generar un sistema de recomendación entre Talentos y proyectos que promueven Organizaciones/Instituciones.

El reporte técnico se encuentra en ```/entregables/reporte_final``` y se compone por las siguientes secciones:

	1. Introducción
	2. Objetivo del proyecto
	3. Estructura de bases de datos
	4. Acercamiento Analítico
	5. Arquitectura de Productos de Datos
	6. Conclusiones
	7. Trabajo futuro
	8. Apéndice

Este reporte se puede visualizar a través de ```R Markdown```.

El sistema de recomendación se ejecuta a través de un producto de datos que se encuentra en ```/infraestructura```, tiene como insumos:

```
	1. /etl
	2. /src
	3. /import

```

La orquestación del flujo de trabajo se ejecuta ```docker-compose --project=fdc up``` en ```/infraestructura```

Los programas requeridos son:

```
	1. docker version 1.11.1 o superior
	2. docker-compose version 1.9.0 o superior

```



