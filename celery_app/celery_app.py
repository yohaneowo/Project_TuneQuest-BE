from celery import Celery
import os
from dotenv_vault import load_dotenv
load_dotenv()

rabbitmq_port = os.getenv("RABBITMQ_PORT")
redis_port = os.getenv("REDIS_PORT")
docker_host = os.getenv("DOCKER_HOST")
print(docker_host)


broker_url = f'amqp://192.168.31.218:{int(rabbitmq_port)}'
backend_url = f'redis://{docker_host}:{int(redis_port)}'

app = Celery(__name__, broker=broker_url , backend=backend_url)
@app.task
def add(x, y):
    return x + y