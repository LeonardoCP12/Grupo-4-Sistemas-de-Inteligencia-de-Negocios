**LABORATORIO N°1**

Integrantes:                                                                                                                                                               Grupo 4

- Cárdenas Palacios, Leonardo Gustavo
- Espinoza Cerna, Alex
- Inocente Caro, Miguel Anderson


Requisitos del ordenador usado

![](imagenes/Aspose.Words.f926092b-9ef6-410d-8fcc-eacb01ecb3dc.001.png)

Instalando Virtual Box

![](imagenes/Aspose.Words.f926092b-9ef6-410d-8fcc-eacb01ecb3dc.002.png)

![](imagenes/Aspose.Words.f926092b-9ef6-410d-8fcc-eacb01ecb3dc.003.png)Ejecutar el instalador de Virtual Box


Luego de dar a la opción de Archivo-Preferencias- General, elegimos llamar al archivo por defectro con el nombre de InteligenciaNegocios

![](imagenes/Aspose.Words.f926092b-9ef6-410d-8fcc-eacb01ecb3dc.004.png)


Importacion del HDP Sandbox

![](imagenes/Aspose.Words.f926092b-9ef6-410d-8fcc-eacb01ecb3dc.005.png)

Infromacion por defecto

![](imagenes/Aspose.Words.f926092b-9ef6-410d-8fcc-eacb01ecb3dc.006.png)



Configurando la red

![](imagenes/Aspose.Words.f926092b-9ef6-410d-8fcc-eacb01ecb3dc.007.png)

Asignando recursos

![](imagenes/Aspose.Words.f926092b-9ef6-410d-8fcc-eacb01ecb3dc.008.png)

![](imagenes/Aspose.Words.f926092b-9ef6-410d-8fcc-eacb01ecb3dc.009.png)

Arrancando el sistema\
![](imagenes/Aspose.Words.f926092b-9ef6-410d-8fcc-eacb01ecb3dc.010.png)


![](imagenes/Aspose.Words.f926092b-9ef6-410d-8fcc-eacb01ecb3dc.011.png)


Accediendo al Ambari desde la dirección: \
\
http://localhost:1080 

![](imagenes/Aspose.Words.f926092b-9ef6-410d-8fcc-eacb01ecb3dc.012.png)

![](imagenes/Aspose.Words.f926092b-9ef6-410d-8fcc-eacb01ecb3dc.013.png)

Para acceder al root\
![](imagenes/Aspose.Words.f926092b-9ef6-410d-8fcc-eacb01ecb3dc.014.png)

![](imagenes/Aspose.Words.f926092b-9ef6-410d-8fcc-eacb01ecb3dc.015.png)



![](imagenes/Aspose.Words.f926092b-9ef6-410d-8fcc-eacb01ecb3dc.016.png)



Servicios principales activos 

HDFS, YARN, Hive, Spark, Zeppelin, como se puede observar en pantalla.

![](imagenes/Aspose.Words.f926092b-9ef6-410d-8fcc-eacb01ecb3dc.017.png)


Ingresamos a la opción del Web Shell Client

![](imagenes/Aspose.Words.f926092b-9ef6-410d-8fcc-eacb01ecb3dc.018.png)

Comrpobacion inicial

![](imagenes/Aspose.Words.f926092b-9ef6-410d-8fcc-eacb01ecb3dc.019.png)

Subiendo archivo csv cuyo nombre es flights.csv y le damos opción files view

![](imagenes/Aspose.Words.f926092b-9ef6-410d-8fcc-eacb01ecb3dc.020.png)



La dirección es user/admin/datasets/flights.csv como se observa en pantalla\
\
![](imagenes/Aspose.Words.f926092b-9ef6-410d-8fcc-eacb01ecb3dc.021.png)

Entramos a la opción Hive view para ingresar la query 

![](imagenes/Aspose.Words.f926092b-9ef6-410d-8fcc-eacb01ecb3dc.022.png)




Cargamos las tablas


![](imagenes/Aspose.Words.f926092b-9ef6-410d-8fcc-eacb01ecb3dc.023.png)

Usamos el siguiente códigopara crear la tabla externa en Hive.

```sql
CREATE EXTERNAL TABLE flights (
  year STRING,
  month STRING,
  day STRING,
  dep_time STRING,
  dep_delay STRING,
  arr_time STRING,
  arr_delay STRING,
  carrier STRING,
  tailnum STRING,
  flight STRING,
  origin STRING,
  dest STRING,
  air_time STRING,
  distance STRING,
  hour STRING,
  minute STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/admin/datasets/flights.csv/'
TBLPROPERTIES ("skip.header.line.count"="1");
```
Una vez creado la  tabla externa en Hive se utiliza cuando deseas que los datos permanezcan fuera del control directo de Hive. Y probamos la query select\*from flights para comprobar el funcionamiento.

![](imagenes/Aspose.Words.f926092b-9ef6-410d-8fcc-eacb01ecb3dc.024.png)



Se genera la siguiente tabla:

![](imagenes/Aspose.Words.f926092b-9ef6-410d-8fcc-eacb01ecb3dc.025.png)




