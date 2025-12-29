import json
import boto3

sf = boto3.client("stepfunctions")

def lambda_handler(event, context):
    # Tomamos bucket y key del evento S3
    s3_bucket = event["Records"][0]["s3"]["bucket"]["name"]
    s3_key = event["Records"][0]["s3"]["object"]["key"]

    # Parámetros que se enviarán a Step Functions
    input_data = {
        "glueArguments": {
            "--bucket": s3_bucket,
            "--txt_key": s3_key
        }
    }

    # ARN de la state machine
    state_machine_arn = "arn:aws:states:us-east-2:772069004820:stateMachine:Step_Function_ETL_tramas"

    sf.start_execution(
        stateMachineArn=state_machine_arn,
        input=json.dumps(input_data)
    )

    return {"status": "OK"}