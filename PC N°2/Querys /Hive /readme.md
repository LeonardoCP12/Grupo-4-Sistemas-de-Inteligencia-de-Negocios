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
