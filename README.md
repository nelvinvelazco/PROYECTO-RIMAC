
 # **REGULARIZACION DE PRIMAS DE LOS PRODUCTOS DE DESGRAVAMEN - BBVA**

 ## 📑`Tabla de Contenido`
1. [Información General](#Información-General)
2. [Arquitectura](#Arquitectura) 
3. [Tecnologías Utilizadas](#tecnologías-Utilizadas)
4. [Data Lake](#data-lake)
5. [Data WareHouse](#data-warehouse)
6. [Visualización](#visualización)

## 📖 `Informacion General`

Los movimientos de transacciones (pagos, bajas, altas, anulaciones) de los clientes de Seguros Rimac son reportados por el banco mediante tramas(linea de texto), las cuales son cargadas al sistema SAS para registrar dichas transacciones en sus bases datos. Algunos de estos registros resultaron en error, por diferentes razones y se fueron acumulando a travez de los años, lo cual provocó inconsistencia en el historial de transacciones de los cliente. Por esta razon se inicio este proyecto que tiene como objetivo analizar los errores para encontrar la mejor manera de regularizarlos o corregirlos

## 🏗️ `Arquitectura`

## ☁️ `Tecnologias Utilizadas`

 - Se utilizó Python version 3.13 y varias librerias como: *`pyspark, pandas, zipfile, json, numpy, os, sys, io, datetime, google.cloud (storage, bigquery), awsglue, boto3`
- Jupyter notebooks.
- GCP (Cloud Storage, BigQuery, Colab notebooks)
- AWS (S3, Glue, Athena, Lambda, Step Functions, EC2, VPC, RedShift, SQS, EventBrigde)
- Power BI
- Power Automate

## `Data Lake`

Se utilizó Cloud Storage como Data Lake en el cual se almaceno todos los archivos crudos de los reportes de errores historicos. Tambien se Utilizo AWS S3 para almacenar "tramas diarias" crudas y las tramas procesadas en formato .parquet.

La data se extrajo directamente de las bases de datos Oracle de SAS, estos se puede visualizar aqui [sql/sas](sql/sas/). Estos se cargaron a un bucket de Cloud Storage organizados por tipo de seguro y fecha de carga. Luego se realizo la limpieza y tranformaciones necesarias a estos datos utilizando scripts de python [src/data](src/data/), los cuales se almacenaban el otro bucket y se enviaban a una base de datos en bigquery

Adicionalmente tambien se cargaron los datos de las tramas diarias al Data WereHouse en bigquery y RedShift de AWS para hacer consultas y extracciones de informacion. Estos script de ETL se puede visualizar aqui [link]

## `Data WareHouse`

Se utilizo BigQuery como WareHouse...

## `Visualización`

Se realizacion varios dashboard para visualizar las categorias de errores de emision de primas
