import boto3
import json

def lambda_handler(event, context):
    glue_client = boto3.client('glue')
    
    try:
        # Extrai informações do evento S3
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        object_key = event['Records'][0]['s3']['object']['key']
        
        # Log para debug
        print(f"Bucket: {bucket_name}, Key: {object_key}")
        
        # Inicia o Glue Job com parâmetros
        response = glue_client.start_job_run(
            JobName='BovespaJob'
        )
        
        return {
            'statusCode': 200,
            'body': f"Job started successfully: {response['JobRunId']}"
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error starting job: {str(e)}"
        }