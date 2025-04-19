import boto3
import os
import json
from dotenv import load_dotenv

load_dotenv()

sqs = boto3.client(
  'sqs',
  aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
  aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
  region_name=os.getenv('AWS_REGION')
)

queue_url = os.getenv('SQS_QUEUE_URL')

def consume_messages():
  try:
    while True:
      print('Consuming messages...')
    
      response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=20,
        VisibilityTimeout=30
      )
      
      if 'Messages' in response:
        for message in response['Messages']:
          try:
            print("Processando mensagem:", message['Body'])
            print("Mensagem processada com sucesso.")
            
            body = json.loads(message['Body'])
            
            sqs.delete_message(
              QueueUrl=queue_url,
              ReceiptHandle=message['ReceiptHandle']
            )
            
            print("Mensagem deletada da fila.")
          except Exception as e:
              print("Erro ao processar mensagem:", e)
      else:
        print("Nenhuma mensagem disponível. Aguardando...")
  except Exception as e:
    print("Erro ao consumir mensagens:", e)
  
if __name__ == '__main__':
  consume_messages()