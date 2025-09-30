# Querys desde el Zeppelin  

## Para la data cruda del Practitioner  

### Mostrar las 5 primeras filas, ver el tipo de dato y conteo de filas.

```pyspark
%pyspark
csv_file = "hdfs:///user/root/data_cruda_practitioner/data_cruda_practitioner.csv"
# Lee el archivo CSV usando el API de Spark
df = spark.read.option("header", "true").option("inferSchema", "true").csv(csv_file)

%pyspark
# Muestra las primeras filas de la data
df.show(5)

%pyspark
# Muestra el esquema de la data (para verificar los tipos de datos inferidos)
df.printSchema()

%pyspark
# Muestra la cantidad de registros de la data
df.count()
```

<img width="886" height="455" alt="image" src="https://github.com/user-attachments/assets/fb670008-c1fc-4983-952a-9e541be0de3e" />

**Nota.** *Queries en Zeppelin: primeras filas, esquema y conteo de registros del practitioner* 

### Cálculo de los 6 KPI’s del Practitioner

```pyspark
%pyspark
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# Agregar un ID de fila para mantener el orden original del CSV
df = df.withColumn("row_id", F.monotonically_increasing_id())

# Crear ventana para obtener datos del mes anterior por servicio
window_prev = Window.partitionBy("geografia", "service1_name").orderBy("mes")

df_calc = (df
    # KPI A.a - RFO OK %
    .withColumn("rfo_ok_pct", F.when(F.col("nro_fichas_rfo") > 0, 
        F.round((F.col("nro_fichas_rfo_ok")/F.col("nro_fichas_rfo"))*100, 2)))
    # KPI A.b - Dependencias %
    .withColumn("dep_pct", F.when(F.col("nro_sn2_sn1") > 0, 
        F.round((F.col("nro_sn2_sn1_dependencias")/F.col("nro_sn2_sn1"))*100, 2)))
    # KPI B.a - Adopción SN2 %
    .withColumn("adopcion_sn2_pct", F.when(F.col("sn2_sn1_medidos") > 0, 
        F.round((F.col("puntaje_total_adopcion_sn2")/F.col("sn2_sn1_medidos"))*100, 2)))
    # KPI C.a - Calidad de features %
    .withColumn("calidad_features_pct", F.when(F.col("nro_features_desplegadas") > 0, 
        F.round((F.col("nro_features_desplegadas_calidad")/F.col("nro_features_desplegadas"))*100, 2)))
    
    # KPI D.a - Vulnerabilidades por mil LOC (actual)
    .withColumn("vuln_actual", 
        F.when(F.col("total_lineas_codigo") > 0, 
            (F.col("total_vulnerabilidades_high")/F.col("total_lineas_codigo"))*1000))
)

# Solo calcular mes anterior si vuln_actual está entre 0.04 y 0.2
df_calc = df_calc.withColumn("necesita_mes_anterior",
    F.when(F.col("total_lineas_codigo") <= 0, False)
     .when(F.col("vuln_actual") < 0.04, False)
     .when(F.col("vuln_actual") > 0.2, False)
     .otherwise(True)
)

# Obtener datos del mes anterior SOLO cuando se necesita
df_calc = (df_calc
    .withColumn("total_vulnerabilidades_high_prev", 
        F.when(F.col("necesita_mes_anterior"), 
            F.lag("total_vulnerabilidades_high").over(window_prev)))
    .withColumn("total_lineas_codigo_prev", 
        F.when(F.col("necesita_mes_anterior"), 
            F.lag("total_lineas_codigo").over(window_prev)))
    
    # Vulnerabilidades por mil LOC (anterior)
    .withColumn("vuln_anterior",
        F.when(~F.col("necesita_mes_anterior"), None)
         .when(F.col("total_lineas_codigo_prev").isNull(), F.lit(-99))
         .when(F.col("total_lineas_codigo_prev") <= 0, F.lit(-99))
         .otherwise((F.col("total_vulnerabilidades_high_prev")/F.col("total_lineas_codigo_prev"))*1000))
    
    # Evolución de vulnerabilidades
    .withColumn("evol_vuln",
        F.when(~F.col("necesita_mes_anterior"), None)
          .when(F.col("vuln_anterior") == -99, None)
          .when(F.col("vuln_anterior") == 0, None)
          .otherwise(((F.col("vuln_actual") - F.col("vuln_anterior"))/F.col("vuln_anterior"))*100))
    
    # KPI D.a - Seguridad %
    .withColumn("seguridad_pct",
        # 1. Si no hay código en mes actual, no se considera
        F.when(F.col("total_lineas_codigo") <= 0, None)
        # 2. Evaluar umbrales absolutos PRIMERO
         .when(F.col("vuln_actual") < 0.04, F.lit(100))
         .when(F.col("vuln_actual") > 0.2, F.lit(0))
        # 3. Si está entre umbrales, evaluar evolución
         .when(F.col("vuln_anterior") == -99, None)
         .when(F.col("evol_vuln").isNull(), None)
         .when(F.col("evol_vuln") == -100, F.lit(0))
         .when(F.col("evol_vuln") <= -10, F.lit(100))
         .when((F.col("evol_vuln") > -10) & (F.col("evol_vuln") < 0), F.lit(75))
         .when(F.col("evol_vuln") == 0, F.lit(50))
         .when((F.col("evol_vuln") > 0) & (F.col("evol_vuln") < 10), F.lit(25))
         .when(F.col("evol_vuln") >= 10, F.lit(0))
         .otherwise(None)
    )
)

# Definición de pesos
pesos = {
    "rfo_ok_pct": 13,
    "dep_pct": 13,
    "adopcion_sn2_pct": 27,
    "calidad_features_pct": 20,
    "seguridad_pct": 27
}

# Construir columnas ponderadas
df_calc = df_calc.withColumn("suma_pesada",
    sum(F.when(F.col(k).isNotNull(), F.col(k)*v).otherwise(0) for k,v in pesos.items())
).withColumn("suma_pesos",
    sum(F.when(F.col(k).isNotNull(), F.lit(v)).otherwise(0) for k,v in pesos.items())
).withColumn("adopcion_total_pct",
    F.when(F.col("suma_pesos") > 0, F.round(F.col("suma_pesada") / F.col("suma_pesos"), 2)).otherwise(None)
)

#Para filtrar de otras formas
#df_calc.filter(F.col("nombre columna") == "nombre especifico").orderBy("row_id").select(

# Mostrar las primeras 20 filas con todas las columnas de KPIs
df_calc.orderBy("row_id").select(
    "mes","geografia","service1_name",
    "rfo_ok_pct","dep_pct","adopcion_sn2_pct","calidad_features_pct",
    "seguridad_pct","adopcion_total_pct"
).show(20, truncate=False)
```

<img width="886" height="884" alt="image" src="https://github.com/user-attachments/assets/8771b872-9915-4a0c-b00b-a38803e59e0d" />

<img width="886" height="575" alt="image" src="https://github.com/user-attachments/assets/25820254-f7e2-4f5a-9964-b3828c46cd5f" />

**Nota.** *Cálculo de los 6 KPI’s del Practitioner en Zeppelin.* 

### Cálculo de los 13 KPI’s del Continuous Integration

```pyspark
%pyspark
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# Agregar un ID de fila para mantener el orden original del CSV
df = df.withColumn("row_id", F.monotonically_increasing_id())

df_calc = (df
    # A.a - % Análisis en estado «Analysis in Review» menor o igual a 7 días
    .withColumn("analisis_review_7dias_pct", 
                F.when(F.col("issues_analysis_in_review") > 0, 
                       F.round((F.col("issues_analysis_in_review_menor_7_dias")/F.col("issues_analysis_in_review"))*100, 2)))
    
    # B.a - % Historias de usuario con Release/FixVersión asociado
    .withColumn("historias_fix_version_pct", 
                F.when(F.col("nro_historias_deployed") > 0, 
                       F.round((F.col("historias_deployed_fix_version")/F.col("nro_historias_deployed"))*100, 2)))
    
    # C.a - % Repositorios con nomenclatura estándar
    .withColumn("repos_nomenclatura_pct", 
                F.when(F.col("total_repositorios_activos") > 0, 
                       F.round((F.col("repositorios_activos_nomenclatura_estandar")/F.col("total_repositorios_activos"))*100, 2)))
    
    # C.b - Tiempo medio de aprobación de Pull Requests
    .withColumn("aprobacion_pr_pct",
                F.when(F.col("tiempo_medio_aprobacion_pr") < 1, F.lit(90))
                 .when((F.col("tiempo_medio_aprobacion_pr") >= 1) & (F.col("tiempo_medio_aprobacion_pr") < 1.5), F.lit(70))
                 .when((F.col("tiempo_medio_aprobacion_pr") >= 1.5) & (F.col("tiempo_medio_aprobacion_pr") < 3), F.lit(30))
                 .when(F.col("tiempo_medio_aprobacion_pr") >= 3, F.lit(0))
                 .otherwise(None))
    
    # C.c - Tamaño Medio de Pull Requests
    .withColumn("tamano_pr_pct",
                F.when(F.col("tamano_medio_pr") < 300, F.lit(90))
                 .when((F.col("tamano_medio_pr") >= 300) & (F.col("tamano_medio_pr") < 400), F.lit(70))
                 .when((F.col("tamano_medio_pr") >= 400) & (F.col("tamano_medio_pr") < 600), F.lit(30))
                 .when(F.col("tamano_medio_pr") >= 600, F.lit(0))
                 .otherwise(None))
    
    # C.d - Repositorios gobernados en el análisis estático de Seguridad
    .withColumn("repos_chimera_pct", 
                F.when(F.col("total_repositorios_activos") > 0, 
                       F.round((F.col("repositorios_activos_gobernados_chimera")/F.col("total_repositorios_activos"))*100, 2)))
    
    # D.a - Tiempo medio de integración
    .withColumn("tiempo_integracion_pct",
                F.when(F.col("tiempo_medio_integracion") < 3, F.lit(90))
                 .when((F.col("tiempo_medio_integracion") >= 3) & (F.col("tiempo_medio_integracion") < 4), F.lit(70))
                 .when((F.col("tiempo_medio_integracion") >= 4) & (F.col("tiempo_medio_integracion") < 6), F.lit(30))
                 .when(F.col("tiempo_medio_integracion") >= 6, F.lit(0))
                 .otherwise(None))
    
    # D.b - Tiempo medio construcciones
    .withColumn("tiempo_construcciones_pct",
                F.when(F.col("tiempo_medio_construcciones") < 20, F.lit(90))
                 .when((F.col("tiempo_medio_construcciones") >= 20) & (F.col("tiempo_medio_construcciones") < 35), F.lit(70))
                 .when((F.col("tiempo_medio_construcciones") >= 35) & (F.col("tiempo_medio_construcciones") < 45), F.lit(30))
                 .when(F.col("tiempo_medio_construcciones") >= 45, F.lit(0))
                 .otherwise(None))
    
    # D.c - % Construcciones correctas
    .withColumn("construcciones_correctas_pct", 
                F.when(F.col("ejecuciones_pipeline") > 0, 
                       F.round((F.col("ejecuciones_pipeline_success")/F.col("ejecuciones_pipeline"))*100, 2)))
    
    # D.d - Tiempo medio en arreglar construcciones
    .withColumn("tiempo_arreglar_construcciones_pct",
                F.when(F.col("tiempo_medio_arreglar_construcciones") < 60, F.lit(90))
                 .when((F.col("tiempo_medio_arreglar_construcciones") >= 60) & (F.col("tiempo_medio_arreglar_construcciones") < 120), F.lit(70))
                 .when((F.col("tiempo_medio_arreglar_construcciones") >= 120) & (F.col("tiempo_medio_arreglar_construcciones") < 180), F.lit(30))
                 .when(F.col("tiempo_medio_arreglar_construcciones") >= 180, F.lit(0))
                 .otherwise(None))
    
    # E.a - Calidad del código
    .withColumn("calidad_codigo_pct", 
                F.when(F.col("repositorios_activos_sonarqube") > 0, 
                       F.round((F.col("repositorios_activos_sonarqube_ok")/F.col("repositorios_activos_sonarqube"))*100, 2)))
    
    # E.b - % Historias de Usuario, Dependencias y Bugs con pruebas de aceptación (XRay)
    .withColumn("items_pruebas_xray_pct", 
                F.when(F.col("items_desplegados") > 0, 
                       F.round((F.col("items_desplegados_pruebas_xray")/F.col("items_desplegados"))*100, 2)))
)

# Definición de pesos (suman 100%)
pesos_ci = {
    "analisis_review_7dias_pct": 5,
    "historias_fix_version_pct": 6,
    "repos_nomenclatura_pct": 6,
    "aprobacion_pr_pct": 10,
    "tamano_pr_pct": 5,
    "repos_chimera_pct": 7,
    "tiempo_integracion_pct": 16,
    "tiempo_construcciones_pct": 9,
    "construcciones_correctas_pct": 13,
    "tiempo_arreglar_construcciones_pct": 8,
    "calidad_codigo_pct": 10,
    "items_pruebas_xray_pct": 5
}

# Construir columnas ponderadas para Continuous Integration
df_calc = df_calc.withColumn("suma_pesada_ci",
    sum(F.when(F.col(k).isNotNull(), F.col(k)*v).otherwise(0) for k,v in pesos_ci.items())
).withColumn("suma_pesos_ci",
    sum(F.when(F.col(k).isNotNull(), F.lit(v)).otherwise(0) for k,v in pesos_ci.items())
).withColumn("adopcion_ci_pct",
    F.when(F.col("suma_pesos_ci") > 0, F.round(F.col("suma_pesada_ci") / F.col("suma_pesos_ci"), 2)).otherwise(None)
)

# FILTRO: Cambia este valor para filtrar por % de adopción mínima
umbral_adopcion = 90

# Mostrar filas filtradas por umbral de adopción
df_calc.filter(F.col("adopcion_ci_pct") >= umbral_adopcion).orderBy("row_id").select(
    "mes","geografia","sn1",
    "analisis_review_7dias_pct","historias_fix_version_pct","repos_nomenclatura_pct",
    "aprobacion_pr_pct","tamano_pr_pct","repos_chimera_pct",
    "tiempo_integracion_pct","tiempo_construcciones_pct","construcciones_correctas_pct",
    "tiempo_arreglar_construcciones_pct","calidad_codigo_pct","items_pruebas_xray_pct",
    "adopcion_ci_pct"
).show(1326, truncate=False)
```

<img width="886" height="466" alt="image" src="https://github.com/user-attachments/assets/70cbaf33-75c0-4415-8952-a977d40de587" />

<img width="886" height="280" alt="image" src="https://github.com/user-attachments/assets/43a28893-a773-4f63-9364-5c8d913b24a0" />

**Nota.** *Cálculo de los 13 KPI’s y adopción total en Continuous Integration.* 







