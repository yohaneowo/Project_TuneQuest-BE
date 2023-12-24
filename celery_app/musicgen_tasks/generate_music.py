from celery_app.celery_app import celery_app
from ai_generation_core.musicgen.musicgen import Musicgen


@celery_app.task()
def generate_music_local():
    print("start")
    x = Musicgen()
    result = x.generate_music()
    return {"status": True , "result": result}

