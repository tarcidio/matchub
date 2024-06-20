import json
import boto3
import base64
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from email.message import EmailMessage

def get_credentials_from_secrets_manager(secret_name, region_name):
    client = boto3.client('secretsmanager', region_name=region_name)
    response = client.get_secret_value(SecretId=secret_name)
    secret_dict = json.loads(response['SecretString'])
    refresh_token = secret_dict['refresh_token']
    client_id = secret_dict['client_id']
    client_secret = secret_dict['client_secret']
    token_uri = secret_dict['token_uri']
    
    credentials = Credentials(
        None,  # No token to start with
        refresh_token=refresh_token, 
        token_uri=token_uri,
        client_id=client_id,
        client_secret=client_secret
    )
    credentials.refresh(Request())
    return credentials

def send_email(service, email, subject, text):
    message = EmailMessage()
    message.set_content(text)
    message['to'] = email
    message['from'] = 'MatcHub <tarcidio.antonio2@gmail.com>'  # Use your actual email address here
    message['subject'] = subject

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    body = {'raw': raw_message}

    try:
        sent_message = service.users().messages().send(userId='me', body=body).execute()
        print('Message Id:', sent_message['id'])
        return sent_message
    except Exception as error:
        print(f'An error occurred: {error}')
        return None

def lambda_handler(event, context):
    secret_name = "GMAILServiceAccountCredentials"  # Update this with your actual secret name
    region_name = "sa-east-1"
    
    
    credentials = get_credentials_from_secrets_manager(secret_name, region_name)
    service = build('gmail', 'v1', credentials=credentials)
    
    print(event)
    
    for record in event['Records']:
        payload = json.loads(record['body'])
        email = payload['email']
        subject = payload['subject']
        text = payload['text']
        
        send_email(service, email, subject, text)

    return {
        'statusCode': 200,
        'body': json.dumps('Emails sent successfully')
    }