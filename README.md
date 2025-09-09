# Grupo-4-Sistemas-de-Inteligencia-de-Negocios

## Integrantes
- Cárdenas Palacios, Leonardo Gustavo
- Espinoza Cerna, Alex
- Inocente Caro, Miguel Anderson

## Empresa
BBVA

## Problematica
Actualmente los indicadores de calidad, seguridad y cumplimiento de los servicios están dispersos en archivos de datos crudos, lo que obliga a revisar línea por línea para identificar vulnerabilidades, dependencias no asignadas o bajo nivel de adopción del modelo operativo. Esta falta de una vista consolidada dificulta que el Service Owner tenga control oportuno sobre el estado real de su servicio, generando riesgos de incumplimiento en la certificación y retrasos en la toma de decisiones de mejora.

## Persona que tiene la problematica
Servive Owner y del área de Ingeniería & Data / Systems Engineering.

## Data y Kpi's
La data es un repositorio de indicadores operativos y técnicos de servicios de TI, que mide su calidad, seguridad y grado de adopción del modelo operativo. Integra métricas como fichas RFO, dependencias, features desplegadas y vulnerabilidades de código. 

1. Inventario (Nucleus/RFO):
- % de fichas RFO en estado “OK”.
- % de servicios con dependencias registradas.

2. Modelo Operativo:
- Cumplimiento de adopción de los servicios de nivel 2 según su prioridad.

3. Calidad de Features:
- % de features tipo Customer/Enabler que cumplen criterios de calidad.

4. Seguridad:
- Evolución de vulnerabilidades críticas por cada 1.000 líneas de código.

## Arquitectura Preliminar
Se escogió el datawarehouse, su propósito deveria ser evaluar y certificar el nivel de madurez de cada servicio, apoyando la gestión del Service Owner.
La arquitectura de Data Warehouse en BBVA resuelve la problemática de tener indicadores dispersos en múltiples fuentes, ya que integra toda la información operativa y técnica de los servicios de TI (RFO, dependencias, features, vulnerabilidades) mediante Docker, Node.js, Hadoop y Spark, y la consolida en un repositorio único; de esta forma, los Service Owners de BBVA pueden acceder en Power BI a dashboards claros y actualizados que les permiten evaluar la calidad, seguridad y nivel de adopción de sus servicios, reduciendo riesgos de incumplimiento y acelerando la toma de decisiones.

![Arquitectura Preliminar BBVA](https://github.com/user-attachments/assets/012e533d-e688-4041-bf63-084e7327ae14)




