# LISTA DE USUARIOS UTILIZADOS Y CAMBIADOS

|   Usuario   | Contraseña |
|:-----------:|:----------:|
|   admin     |  s4ndb0x7  |
|   root      |  s4ndb0x7  |
| maria_dev   | maria_dev  |

* Nota: Primero se tiene que cambiar las contraseñas.

# Resumen

El trabajo aborda la implementación de un sistema de **Inteligencia de Negocios (BI)** en **BBVA** para mejorar el proceso de certificación de servicios tecnológicos, actualmente gestionado de forma manual y con información dispersa en múltiples fuentes como *Jira, Bitbucket, Nucleus, Jenkins, Chimera y SonarQube*.  

Se utilizó la **metodología Hefesto**, que inicia con la formulación de preguntas de negocio alineadas a las necesidades organizacionales, especialmente del área de **Engineering**, responsable de la gestión y madurez de los servicios digitales. Estas preguntas se enfocaron en el cumplimiento de **17 KPIs**, relacionados con seguridad, calidad, eficiencia y continuidad operativa.  

El marco de referencia aplicado fue el **Playbook de BBVA**, que establece niveles progresivos de madurez tecnológica (*Starting, Growing, Excelling, Practitioner, Continuous Integration, Continuous Delivery y Deployment*). El objetivo principal fue **automatizar el cálculo de KPIs y la certificación**, reemplazando procesos manuales por un **dashboard dinámico** que permita monitoreo en tiempo real y reducción de errores.  

Se diseñaron dos modelos conceptuales en estrella (*star schema*):  

- **Nivel Practitioner**: mide indicadores como número de fichas RFO, dependencias asignadas, features desplegadas y vulnerabilidades detectadas.  
- **Nivel Continuous Integration (CI)**: abarca KPIs como tiempo de aprobación de pull requests, nomenclatura de repositorios, tiempo medio de integración y construcción.  

El inventario de **fuentes OLTP** identificó y clasificó los sistemas transaccionales internos y externos que alimentan los KPIs. Cada fuente fue descrita en cuanto a área usuaria, tipo de sistema, tecnología y frecuencia de actualización.  

Finalmente, se implementó el **ecosistema técnico con Hortonworks (Ambari, HDFS, Hive)** para la ingesta de datasets, creación de tablas y consultas de control, demostrando la viabilidad del enfoque para integrar datos dispersos y convertirlos en información estratégica para la toma de decisiones.  

## Conclusión

El proyecto permite a **BBVA**:  
- Automatizar la certificación tecnológica.  
- Mejorar la trazabilidad, seguridad y eficiencia operativa.  
- Fortalecer la madurez digital de sus servicios mediante un sistema de **BI robusto y escalable**.  
