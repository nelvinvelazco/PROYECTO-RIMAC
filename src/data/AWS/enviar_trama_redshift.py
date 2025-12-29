import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue import DynamicFrame

## Paramentros
args = getResolvedOptions(sys.argv, ['JOB_NAME','input_path'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

## Leer datos procesados desde S3 (Parquet)
s3_path = args['input_path']

# Variable para coneccion a redshift
connection_name = "redshift-conexion2"
redshift_db = "dev"
redshift_table = "public.tramas_diarias_text"

# Script generated for node Amazon S3
df_s3 = glueContext.create_dynamic_frame.from_options(
    format_options={}, connection_type="s3", format="parquet", 
    connection_options={"paths": [s3_path], "recurse": True}
)

# Script generated for node Amazon Redshift
glueContext.write_dynamic_frame.from_options(
    frame=df_s3, 
    connection_type="redshift", 
    connection_options={
            "redshiftTmpDir": "s3://aws-glue-assets-772069004820-us-east-2/temporary/", 
            "useConnectionProperties": "true", 
            "dbtable": redshift_table, 
            "connectionName": connection_name, 
            "preactions": f"CREATE TABLE IF NOT EXISTS {redshift_table} (certificado VARCHAR, fecha_de_afiliacion DATE, fecha_de_inicio_del_seguro DATE, fecha_fin_del_seguro DATE, moneda VARCHAR, numero_interno_del_canal VARCHAR, periodo_de_pago VARCHAR, plan_de_seguro VARCHAR, prima VARCHAR, tipo_de_movimiento VARCHAR, tipo_de_registro VARCHAR, tipo_de_seguro VARCHAR, trama_original VARCHAR, fecha_trama DATE, prima_bruta DOUBLE PRECISION);"
    }
)

job.commit()