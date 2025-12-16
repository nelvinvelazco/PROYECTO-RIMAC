
 # **REGULARIZACION DE PRIMAS DE LOS PRODUCTOS DE DESGRAVAMEN - BBVA**

 ##  `Tabla de Contenido`
1. [Información General](#Información-General)
2. [Tecnologías Utilizadas](#tecnologías-Utilizadas)
3. [Data Lake](#data-lake)
3. [Data WareHouse](#data-warehouse)
7. [Visualización](#visualización)

## `Informacion General`

#### Los movimientos de transacciones (pagos, bajas, altas, anulaciones) de los clientes de Seguros Rimac son reportado por el banco mediante tramas(linea de texto), las cuales son cargadas al sistema SAS para registrar dichas transacciones en las bases del sistema. Algunas de estos registros resultaron en error, por diferentes razones, y se fueron acumulando a travez de los años, lo cual provoco inconsistencia en el historias de transacciones de los cliente. Por esta razon se inicio este proyecto con la finalidad analizar los errores para encontrar la mejor manera de regularizarlos o corregirlos

## `Tecnologias Utilizadas`

#### - Se utilizó Python version 3.11 y varias librerias como: *`Pandas, zipfile, json, numpy, os, datetime, google.cloud(storage, bigquery), `
#### - Jupyter notebooks.
#### - GCP (Cloud Storage, BigQuery)
#### - AWS (S3, Glue, Athena, Lambda, Step Functions, EC2, VPC, RedShift, SQS, EventBrigde)

## `Data Lake`

#### Se utilizo Cloud Storage como Data Lake en el cual se almaceno todos los archivos crudos de los reportes de errores historicos. 
#### Tambien se Utilizo AWS S3 para almacenar "tramas diarias" crudas y las tramas procesadas en formato .parquet

## `Data WareHouse`

#### Se utilizo BigQuery como WareHouse...


## `Visualización`

#### Se realizacion varios dashboard para visualizar las categorias de errores de emision de primas
