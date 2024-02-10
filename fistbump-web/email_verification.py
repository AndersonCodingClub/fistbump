import os
import boto3
from dotenv import load_dotenv


load_dotenv('config.env')

def send_email(send_to_email: str, subject: str, content: str):
    client = boto3.client(
        'ses',
        region_name='us-east-1',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
        aws_secret_access_key=os.environ['AWS_SECRET_KEY'],
    )
    
    response = client.send_email(
        Destination={
            'ToAddresses': [
                send_to_email,
            ],
        },
        Message={
            'Body': {
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': content,
                },
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': subject,
            },
        },
        Source='Fistbump <noreply@fistbump.club>',
    )
    
    return response
    
if __name__ == '__main__':
    send_email('zainmfj@gmail.com', 'Test Email', 'Test Fistbump Email')