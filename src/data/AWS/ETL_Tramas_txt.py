import sys
import os
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
#from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job

import boto3
import io
import re
import json
from zoneinfo import ZoneInfo
from datetime import datetime
from pyspark.sql.functions import to_date, lit, regexp_replace, substring, when, udf, col
from pyspark.sql.types import DoubleType

## Parametros
args = getResolvedOptions(sys.argv, ['JOB_NAME','bucket','txt_key'])

sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
spark.conf.set("spark.sql.parquet.datetimeRebaseModeInWrite", "LEGACY")
spark.conf.set("spark.sql.parquet.datetimeRebaseModeInRead", "LEGACY")

job.init(args['JOB_NAME'], args)

#---- Parametros --------------------------
bucket = args['bucket']
txt_key = args['txt_key']
job_run_id = sys.argv[sys.argv.index('--JOB_RUN_ID') + 1]

# Cliente S3
s3 = boto3.client("s3")

# Descargar el archivo como binario
response = s3.get_object(Bucket=bucket, Key=txt_key)

espacios_col = [(0, 3), (3, 23), (23, 43), (43,45), (45, 48), (48, 49), (368, 376), (376, 384), (384, 392), (346, 347), (639, 641), (411, 426)]
column_names = ["Tipo de seguro", "Certificado", "Numero Interno Del Canal", "Tipo de Registro", "Moneda",
                "Tipo de Movimiento", "Fecha de Afiliacion", "Fecha de inicio del seguro", "Fecha fin del seguro",
                "Periodo de pago", "Plan de Seguro", "Prima"]

# Diccionario de reemplazo
letra = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ{0123456789")
valor = list("1234567891234567890000000000123456789")
diccionario_reemplazo = dict(zip(letra, valor))

# Broadcast para eficiencia
#sc = spark.sparkContext
diccionario_broadcast = sc.broadcast(diccionario_reemplazo)


def convertir_linea(linea):
    row = {name: linea[start:end].strip() for (start, end), name in zip(espacios_col, column_names)}
    row["Trama Original"] = linea
    return row


def extraer_fechas(filename):
    base = filename.split("/")[-1].split(".")[0]
    try:
        fecha_trama = datetime.strptime(base[3:9], "%d%m%y").date()
        dia, mes = int(base[10:12]), int(base[12:14])
        fecha_declarada = datetime(fecha_trama.year, mes, dia).date()
    except:
        fecha_trama, fecha_declarada = None, None
    return fecha_trama, fecha_declarada

def convertir_a_fecha(df, nombre_columna):
    df = df.withColumn(nombre_columna, col(nombre_columna).cast("string"))
    df = df.withColumn(nombre_columna, regexp_replace(nombre_columna, r"\.0$", ""))
    df = df.withColumn(nombre_columna, substring(nombre_columna, 1, 8))
    df = df.withColumn(nombre_columna, when(col(nombre_columna).rlike(r"^\d{8}$"), col(nombre_columna)).otherwise(None))
    df = df.withColumn(nombre_columna, to_date(nombre_columna, "yyyyMMdd"))
    return df

def convertir_prima(valor_str):
    try:
        if not isinstance(valor_str, str) or len(valor_str) < 2:
            return None
        parte_numerica = valor_str[:-1]
        letra_final = valor_str[-1]
        digito = diccionario_broadcast.value.get(letra_final)
        if digito is None:
            return None
        numero_str = parte_numerica + digito
        return float(numero_str) / 100
    except:
        return None

convertir_prima_udf = udf(convertir_prima, DoubleType())

# Cargar el archivo en memoria
file_content = response['Body'].read().decode("latin-1")
lines = file_content.splitlines()
rdd = spark.sparkContext.parallelize(lines)
       
df_rdd = rdd.map(convertir_linea)
df = spark.createDataFrame(df_rdd)

fecha_trama, fecha_declarada = extraer_fechas(txt_key)
df = df.withColumn("Fecha Trama", to_date(lit(str(fecha_trama)), "yyyy-MM-dd"))
df = df.withColumn("Fecha Declarada", to_date(lit(str(fecha_declarada)), "yyyy-MM-dd"))
        
df = df.withColumn("Prima Bruta", convertir_prima_udf(df["Prima"]))
df = convertir_a_fecha(df, "Fecha de Afiliacion")
df = convertir_a_fecha(df, "Fecha de inicio del seguro")
df = convertir_a_fecha(df, "Fecha fin del seguro")
columnas_originales = df.columns
columnas_limpias = [col.strip().upper().replace(" ", "_") for col in columnas_originales]
columnas_limpias = [re.sub(r'[^A-Z0-9]', '_', col) for col in columnas_limpias]
        
for old, new in zip(columnas_originales, columnas_limpias):
    df = df.withColumnRenamed(old, new)
    
timestamp = datetime.now(ZoneInfo("America/Lima")).strftime("%Y-%m-%d_%H-%M-%S")
ruta_destino= f"s3://tramasdiarias-procesadas/tramas_diarias/{timestamp}/"
result = {"output_path": ruta_destino}

# Guardar en s3 en formato spark
df.write.mode("append").parquet(ruta_destino)

s3.put_object(
    Bucket= "tramasdiarias-procesadas",
    Key= f"job_outputs/{job_run_id}.json",
    Body=json.dumps(result)
)
job.commit()