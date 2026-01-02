<p align="center">
  <img src="src/capturas/logo rimac.png" width="500">
</p>  

 # **REGULARIZACION DE PRIMAS DE LOS PRODUCTOS DE DESGRAVAMEN - BBVA**

## 📖 `Descripcion General`

Los movimientos de transacciones (pagos, bajas, altas, anulaciones) de los clientes de Seguros Rimac son reportados por el banco mediante tramas(linea de texto), las cuales son cargadas al sistema SAS para registrar dichas transacciones en sus bases datos. Algunos de estos registros resultaron en error, por diferentes razones y se fueron acumulando a travez de los años, lo cual provocó inconsistencia en el historial de transacciones de los cliente. Por esta razon se inicio este proyecto que tiene como objetivo analizar los errores para encontrar la mejor manera de regularizarlos o corregirlos

## 🏗️ `Arquitectura`
<p align="left">
  <img src="src/capturas/Arquitectura GCP.png" width="600">
</p> 

<p align="left">
  <img src="src/capturas/Arquitectura AWS.png" width="800">
</p> 

-  **Ingesta de datos desde fuentes externas.**  
    Se extrayeron los datos historicos de los errores de emision de primas mediante un query que extraía los datos desde la bases de datos en Oracle y se exportaban a archivos excel
- **Procesamiento y transformación con Python y Spark.**  
    Se construyo un script en python para limpiar y hacer transformaciones a los archivos procesados. Tambien se desarrollo un script de pyspark para procesar las tramas diarias que se disponian en archivos .TXT
- **Almacenamiento en Data Lake / Data Warehouse.**  
    Se utilizó Cloud Storage como Data Lake en el cual se almaceno todos los archivos crudos de los reportes de errores historicos. Tambien se Utilizo AWS S3 para almacenar "tramas diarias" crudas y las tramas procesadas en formato .parquet.
    Los datos de los errores procesados se almacenaron en el Data Warehouse en una base de Datos en BigQuery y en Redshift de AWS
- **Visualización y análisis en Power BI.**    
    Los dashboard de visualizaciones de datos para analsis se hicieron en power BI

## ☁️ `Tecnologías Utilizadas`

- **GCP**  
Cloud Storage, BigQuery, Colab notebooks
- **AWS**  
S3, Glue, Athena, Lambda, Step Functions, EC2, VPC, RedShift, SQS, EventBrigde
- **Lenguajes**  
Se utilizó Python version 3.13 y varias librerias como: *pyspark, pandas, zipfile, json, numpy, os, sys, io, datetime, google.cloud (storage, bigquery), awsglue, boto3*. 
_ SQL
- **Otros**  
_ Jupyter notebooks.  
_ Power BI.  
_ Power Automate.  


## 🔄 `Flujo de Datos (Data Pipeline)`
1. **Ingesta de datos crudos en Cloud Storage / S3**

- La data del reporte de errores se extrajo directamente de las bases de datos Oracle de SAS mediante [querys](sql/sas/). Estos se cargaron a un bucket de Cloud Storage organizados por tipo de seguro y fecha de carga.  
- Tambien se cargaron los datos de las tramas diarias en S3 de AWS.

2. **Procesamiento y limpieza con Python / PySpark**
- Se realizaron pipelines para el ETL en python y pyspark en [notebook](notebooks/). Luego se realizaron diferentes [script](src/data/GCP/) para ser ejecutados desde colab con el se realizo el enlace con los servicios de GCP utilizados.
- Se automatizo el proceso de ETL de las tramas diarias ulizando un [pipeline](src/data/AWS/) donde se usaron servicios de AWS como S3, EventBrigde, Lambda Stepfuncion, glue, entre otros.

3. **Carga de datos transformados en BigQuery / Redshift**
- Se utilizó como Data WareHouse BigQuery y Redshift, desde donde se hicieron [querys](sql/querys/) de SQL para hacer consultas especificas haciendo uniones, agregaciones y [vistas](sql/vistas/) para exportar datos o para ser usadas en los dashboard de analisis en Power BI.

4. **Visualización en Power BI**
 - Se crearon varios dasboard para [visualizar](src/visualizaciones/) el ranking de errores por cantidad y por Montos de prima involucrada. Con este analisis se pudo organizar y priorizar los errores que se iban a regularizar por facilidad de solucion y cantidad de prima que generaban.  

 Aqui se muestran algunos pantallazos de estas visualizaciones:


