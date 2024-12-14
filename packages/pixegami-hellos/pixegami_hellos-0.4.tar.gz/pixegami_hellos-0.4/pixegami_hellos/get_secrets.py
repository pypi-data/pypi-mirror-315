# import boto3
# import json
# from botocore.exceptions import ClientError
# import pandas as pd


# def get_secret(secret_name, env='DEVELOPMENT'):
#     secret_name = secret_name
#     region_name = "us-east-1"

#     # Create a Secrets Manager client
#     session = boto3.session.Session()

#     client = session.client(
#             service_name='secretsmanager',
#             region_name=region_name)

#     try:
#         get_secret_value_response = client.get_secret_value(
#             SecretId=secret_name
#         )
#     except ClientError as e:
#         # For a list of exceptions thrown, see
#         # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
#         raise e

#     # Decrypts secret using the associated KMS key.
#     secret = get_secret_value_response['SecretString']
#     secret_dict = json.loads(secret)
#     return secret_dict


# CREDS = get_secret("camdb_updates")
# AWS_CREDS = get_secret("SecondaryPayer")
# AZR_CREDS = get_secret("utilities_azure")
# AZR_API_CREDS =get_secret("Azure_Client_creds")

