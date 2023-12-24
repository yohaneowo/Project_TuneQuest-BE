from celery_app.celery_app_1 import celery_app_1
from celery_app.celery_app_2 import celery_app_2
from ai_generation_core.musicgen.musicgen import Musicgen


#
@celery_app_1.task()
def generate_music_celery_1():
    # for local model
    print("start")
    x = Musicgen()
    result = x.generate_music()
    return {"status": True , "result": result}

@celery_app_2.task()
def generate_music_celery_2():
    # for replicate model
    print("start")
    x = Musicgen()
    result = x.generate_music()
    return {"status": True , "result": result}

