import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
spark.conf.set("spark.sql.parquet.datetimeRebaseModeInWrite", "LEGACY")
spark.conf.set("spark.sql.parquet.int96RebaseModeInWrite", "LEGACY")

job.init(args['JOB_NAME'], args)

# Ruta donde ya tienes tus archivos Parquet
output_path = "s3://tramasdiarias-procesadas/parquet/"

# Crear la base si no existe
spark.sql("CREATE DATABASE IF NOT EXISTS tramasdiarias_db")

spark.sql("""
CREATE EXTERNAL TABLE IF NOT EXISTS tramasdiarias_db.tramas_diarias (
    CERTIFICADO STRING,
    FECHA_DE_AFILIACION DATE,
    FECHA_DE_INICIO_DEL_SEGURO DATE,
    FECHA_FIN_DEL_SEGURO DATE,
    MONEDA STRING,
    NUMERO_INTERNO_DEL_CANAL STRING,
    PERIODO_DE_PAGO STRING,
    PLAN_DE_SEGURO STRING,
    PRIMA STRING,
    TIPO_DE_MOVIMIENTO STRING,
    TIPO_DE_REGISTRO STRING,
    TIPO_DE_SEGURO STRING,
    TRAMA_ORIGINAL STRING,
    FECHA_TRAMA DATE,
    PRIMA_BRUTA DOUBLE
)
PARTITIONED BY (FECHA_DECLARADA DATE)
STORED AS PARQUET
LOCATION 's3://tramasdiarias-procesadas/parquet/'
TBLPROPERTIES ('parquet.compression'='snappy')
""")

spark.sql("MSCK REPAIR TABLE tramasdiarias_db.tramas_diarias")

job.commit()