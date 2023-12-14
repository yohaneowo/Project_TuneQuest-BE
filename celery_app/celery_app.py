from celery import Celery
import os
from dotenv_vault import load_dotenv
load_dotenv()

rabbitmq_port = os.getenv("RABBITMQ_PORT")
fastapi_port = os.getenv("FASTAPI_PORT")
docker_host = os.getenv("DOCKER_HOST")
print(docker_host)


broker_url = f'amqp://{docker_host}:{int(rabbitmq_port)}'
backend_url = f'http://localhost:{int(fastapi_port)}'

app = Celery(__name__, broker=broker_url)
@app.task
def add(x, y):
    return x + y