import os
import boto3
import string
import random as rd
from dotenv import load_dotenv


load_dotenv('config.env')

def generate_random_code() -> str:
    character_sample_space = [str(x) for x in range(10)] + list(string.ascii_uppercase)
    return ''.join(rd.choices(character_sample_space, k=6))

def get_email_template():
    with open('templates/email_template.html', 'r', encoding='utf-8') as file:
        return file.read()

def send_verification_email(send_to_email: str, name: str, verification_code: str):
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
                'Html': {
                    'Charset': 'UTF-8',
                    'Data': get_email_template().replace('{{verification_code}}', verification_code).replace('{{name}}', name),
                },
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': 'Fistbump account verification',
            },
        },
        Source='Fistbump <noreply@fistbump.club>',
    )
    
    return response
    
if __name__ == '__main__':
    send_verification_email('zainmfj@gmail.com', 'Zain Javaid', generate_random_code())