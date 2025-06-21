import pika
import json
import uuid
import os
import time
from dotenv import load_dotenv

def wait_for_rabbitmq():
    retries = 10
    while retries > 0:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=os.getenv('RABBITMQ_HOST'),
                port=int(os.getenv('RABBITMQ_PORT')),
                credentials=pika.PlainCredentials(
                    os.getenv('RABBITMQ_USERNAME'),
                    os.getenv('RABBITMQ_PASSWORD')
                )
            ))
            connection.close()
            print("[✔] RabbitMQ is ready!")
            return
        except Exception as e:
            print(f"[!] Waiting for RabbitMQ... ({retries} retries left)")
            time.sleep(5)
            retries -= 1
    raise Exception("[✘] RabbitMQ did not start in time.")

class RpcGateway:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host = os.getenv('RABBITMQ_HOST'),
            port = os.getenv('RABBITMQ_PORT'),
            credentials = pika.PlainCredentials(
                os.getenv('RABBITMQ_USERNAME'),
                os.getenv('RABBITMQ_PASSWORD')
            )
        ))
        self.channel = self.connection.channel()
        
        self.channel.queue_declare(queue='queue_gateway')
        self.channel.queue_declare(queue='queue_trainer')
        self.channel.queue_declare(queue='queue_forecaster')
        
        self.channel.basic_consume(
            queue='queue_gateway',
            on_message_callback=self.on_request)
        
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_worker_response,
            auto_ack=True)
        
        self.pending_requests = {}

    def on_request(self, ch, method, props, body):
        request = json.loads(body)
        type = request['type']
        
        request_id = str(uuid.uuid4())
        self.pending_requests[request_id] = {
            'reply_to': props.reply_to,
            'correlation_id': props.correlation_id
        }
        
        worker_queue = f'queue_{type}'
        self.channel.basic_publish(
            exchange='',
            routing_key=worker_queue,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=request_id
            ),
            body=json.dumps(request['payload']))
        
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def on_worker_response(self, ch, method, props, body):
        original_request = self.pending_requests.pop(props.correlation_id)
        
        self.channel.basic_publish(
            exchange='',
            routing_key=original_request['reply_to'],
            properties=pika.BasicProperties(
                correlation_id=original_request['correlation_id']
            ),
            body=body)

    def start(self):
        print("[!] Gateway awaiting requests")
        self.channel.start_consuming()

if __name__ == '__main__':
    load_dotenv()
    wait_for_rabbitmq()
    RpcGateway().start()