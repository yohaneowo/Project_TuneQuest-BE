from celery_app.celery_app import celery_app
from local_model import generate_musicByLocal

@celery_app.task()
def generate_musicByLocal():
    print("start")
    result =  generate_musicByLocal()
    return {"status": True , "result": result}

