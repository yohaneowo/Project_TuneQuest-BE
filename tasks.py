from celery import Celery
app = Celery('tasks', broker='amqp://192.168.31.218:5672//', backend='rpc://')


@app.task
def add(x, y):
    return x + y