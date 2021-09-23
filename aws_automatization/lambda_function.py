import boto3
import urllib
import logging
import sys
import time

logger_app_name = "BatchPred"
logger = logging.getLogger(logger_app_name)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
consoleHandle = logging.StreamHandler(sys.stdout)
consoleHandle.setLevel(logging.INFO)
consoleHandle.setFormatter(formatter)

session = boto3.Session()
ecs_client = boto3.client('ecs')
env_ = 'prod'


    
def build_rec_source(rec):
    source_bucket = rec['s3']['bucket']['name']
    source_key = urllib.parse.unquote_plus(rec['s3']['object']['key'])
    object_size = rec['s3']['object']['size']
    source_object_name = source_key[source_key.rfind('/') + 1:]
    source_full_path = f"s3://{source_bucket}/{source_key}"
    return {
            'bucket': source_bucket,
            'key': source_key,
            'object_name': source_object_name,
            'full_path': source_full_path,
            'env_': env_,
            "object_size": object_size
        }


def run_task(client=ecs_client, **filargs):
    logger.info("Levantando tarea del fargate...")
    deploy_env = filargs.get('env_')
    key = filargs.get('full_path')
    print(key)
    try:
        response = client.run_task(
            cluster='datadayprod' ,
            #launchType='FARGATE',
            capacityProviderStrategy=[
                    {
                        'capacityProvider': "FARGATE_SPOT",
                        'weight': 1,
                        'base': 1
                    },
                ],
            taskDefinition='prueba',
            overrides={
                'containerOverrides': [{
                    'name': 'prueba',
                    'environment': [
                        {
                            'name': 'PROCESO',
                            'value': 'Predecir'
                        },
                        {
                            'name': 'KEY',
                            'value': key
                        }
                    ]
                }]
            },
            count=1,
            platformVersion='LATEST',
            networkConfiguration={
                'awsvpcConfiguration': {
                    'subnets': [
                        "subnet-0c3e7a6d5c7337ea1",
                        "subnet-079744ced0418720b"
                    ],
                    'securityGroups': ['sg-0e4dbd0f69bdc020c'],
                    'assignPublicIp': 'ENABLED'
                }
            }
        )
        # print(response)
        return response
    except Exception as e:
        raise e
def lambda_handler(event, context):
    print(event)
    recs = event.get('Records')
    print(recs)
    recs_len = len(recs)
    logger.info(f"Llegaron: {recs_len} eventos")
    for rec in recs:
        time.sleep(5)  
        source_args = build_rec_source(rec)
        logger.info(f"{source_args.get('key')}")
    
        try:
            run_task_response = run_task(**source_args)
            logger.info("Tarea ejecutada...")
            respuesta = {
                    'statusCode': 200,
                    'body': {
                    'mensaje': 'Se recibio un archivo para ser transformado'
                        }
                    }
            logger.info("Run Task Response: ")
            return respuesta
        except Exception as e:
                logger.info(f"Error: {e}")
        
    return {
        'statusCode': 200,
        'body': {
            'mensaje': 'Nada por hacer'
        }
    }