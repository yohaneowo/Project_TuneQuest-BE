from celery_app import app

@app.task
def add(x, y):
    return x + y

