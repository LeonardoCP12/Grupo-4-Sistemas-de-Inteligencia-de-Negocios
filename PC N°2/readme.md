# LISTA DE USUARIOS UTILIZADOS Y CAMBIADOS

|   Usuario   | Contraseña |
|:-----------:|:----------:|
|   admin     |  s4ndb0x7  |
|   root      |  s4ndb0x7  |
| maria_dev   | maria_dev  |

* Nota: Primero se tiene que cambiar las contraseñas.

# Resumen

# Implementación de un Sistema de BI en BBVA para la Certificación de Servicios Tecnológicos  

El trabajo aborda la implementación de un sistema de **Inteligencia de Negocios (BI)** en **BBVA** para mejorar el proceso de certificación de servicios tecnológicos, actualmente gestionado de forma manual y con información dispersa en múltiples fuentes como *Jira, Bitbucket, Nucleus, Jenkins, Chimera y SonarQube*.  

---

## Metodología y Marco de Referencia  

Se utilizó la **metodología Hefesto**, que inicia con la formulación de preguntas de negocio alineadas a las necesidades organizacionales, especialmente del área de **Engineering**, responsable de la gestión y madurez de los servicios digitales. Estas preguntas se enfocaron en el cumplimiento de **17 KPIs**, relacionados con seguridad, calidad, eficiencia y continuidad operativa.  

El marco de referencia aplicado fue el **Playbook de BBVA**, que establece niveles progresivos de madurez tecnológica (*Starting, Growing, Excelling, Practitioner, Continuous Integration, Continuous Delivery y Deployment*).  

El objetivo principal fue **automatizar el cálculo de KPIs y la certificación**, reemplazando procesos manuales por un **dashboard dinámico** que permita monitoreo en tiempo real y reducción de errores.  

---

## Arquitectura y Flujo de Datos  

Se implementaron mejoras significativas en la **arquitectura de ingesta de datos**.  

1. **Preingesta**: la información proveniente de diversas fuentes se centralizó en el marco **Playbook de BBVA**, desde donde se extrajeron los archivos en formato **CSV** (data cruda).  
2. **Modelo Medallion con Spark**:  
   - **Capa Bronce → Plata**: la data cruda fue procesada y limpiada. Se utilizó **Power BI** para la depuración y estandarización de los datos.  
   - **Capa Plata → Oro**: una vez enriquecida y validada, la información se organizó en un **modelo estrella (star schema)** para soportar el análisis de KPIs.  
3. **DataMart**: se gestionó un almacén de datos especializado para la aplicación en desarrollo, asegurando consistencia y escalabilidad.  
4. **Visualización**: los KPIs se mostraron en un **dashboard en Power BI**, con una **interfaz en React** lista para desplegarse en múltiples plataformas, tanto en dispositivos móviles como en PC.  

### Diagrama del Flujo de Datos  

<img width="4982" height="2314" alt="image" src="https://github.com/user-attachments/assets/d15ab48f-8b5a-496d-aa62-598e901fcf6c" />

