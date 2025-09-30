# Conectar Hive con HDFS  

## Para la data cruda del Practitioner  

```sql
CREATE EXTERNAL TABLE data_cruda_practitioner (   
    mes STRING, 
    geografia STRING, 
    uol1_name STRING, 
    uol2_name STRING, 
    service1_id INT, 
    service1_name STRING, 
    nro_fichas_rfo INT, 
    nro_fichas_rfo_ok INT, 
    nro_sn2_sn1_dependencias INT, 
    nro_sn2_sn1 INT, 
    nro_features_desplegadas_calidad INT, 
    nro_features_desplegadas INT, 
    puntaje_total_adopcion_sn2 DOUBLE, 
    sn2_sn1_medidos INT, 
    total_vulnerabilidades_high INT, 
    total_lineas_codigo INT 
) 
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY ',' 
STORED AS TEXTFILE 
LOCATION '/user/root/data_cruda_practitioner/' 
TBLPROPERTIES ("skip.header.line.count"="1");
```

<img width="886" height="379" alt="image" src="https://github.com/user-attachments/assets/71cfb2c1-d67d-44ac-aa86-17c45c6e3a09" />

**Nota.** *Interfaz Query Editor con la query de la tabla externa del practitioner* 

```sql

select * from data_cruda_practitioner

```

<img width="886" height="545" alt="image" src="https://github.com/user-attachments/assets/aea2234d-de19-4886-bc66-f739bbde04ca" />

**Nota.** *Interfaz Query Editor con la query para ver tabla externa del practitioner* 

## Para la data cruda del Continuous Integration

```sql
CREATE EXTERNAL TABLE data_cruda_continuous_integration (   
    mes STRING, 
    geografia STRING, 
    uol1_name STRING, 
    uol2_name STRING, 
    service1_id INT, 
    sn1 STRING, 
    issues_analysis_in_review_menor_7_dias INT, 
    issues_analysis_in_review INT, 
    historias_deployed_fix_version INT, 
    nro_historias_deployed INT, 
    repositorios_activos_nomenclatura_estandar DOUBLE, 
    total_repositorios_activos INT, 
    tiempo_medio_aprobacion_pr DOUBLE, 
    tamano_medio_pr DOUBLE, 
    repositorios_activos_gobernados_chimera INT, 
    tiempo_medio_integracion DOUBLE, 
    tiempo_medio_construcciones DOUBLE, 
    ejecuciones_pipeline_success INT, 
    ejecuciones_pipeline INT, 
    tiempo_medio_arreglar_construcciones DOUBLE, 
    repositorios_activos_sonarqube_ok INT, 
    repositorios_activos_sonarqube INT, 
    items_desplegados_pruebas_xray INT, 
    items_desplegados INT 
) 
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY ',' 
STORED AS TEXTFILE 
LOCATION '/user/root/data_cruda_continuous_integration/' 
TBLPROPERTIES ("skip.header.line.count"="1");
```
<img width="886" height="386" alt="image" src="https://github.com/user-attachments/assets/d13b3655-39da-43de-836b-49212b5fa41e" />

**Nota.** *Interfaz Query Editor con la query de la tabla externa del continuous integration* 

```sql
select * from data_cruda_continuous_integration

```

<img width="886" height="550" alt="image" src="https://github.com/user-attachments/assets/45628e95-5a4e-4ada-a895-a30c5dbf5b91" />

**Nota.** *Interfaz Query Editor con la query para ver tabla externa del continuous integration* 
