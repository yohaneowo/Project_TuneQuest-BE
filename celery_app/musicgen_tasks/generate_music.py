from celery_app.celery_app import celery_app
from celery_app.celery_app_2 import celery_app_2
from ai_generation_core.musicgen.musicgen import Musicgen
import os

#
@celery_app.task()
def generate_music(prompt: str, duration: int):
    ## dummy value
    generate_method = "replicate"
    top_k = 0.0
    top_p = 0.0
    temperature = 0.0
    continuation = False
    model_version = "facebook/musicgen-melody"
    output_format = "wav"
    continuation_start = 0
    multi_band_diffusion = False
    normalization_strategy = "none"
    classifier_free_guidance = 0
    audiofile_path = ""
    mission_id = ""
    ##

    print("start_task")

    check_file2 = os.path.isfile("./bach.mp3")
    if check_file2:
        print("file exist")
    musicGen_instance = Musicgen(generate_method, top_k, top_p, prompt, duration, temperature, continuation, model_version, output_format, continuation_start, multi_band_diffusion, normalization_strategy, classifier_free_guidance, audiofile_path, mission_id)
    result = musicGen_instance.generate_music()
    print(result)
    print("here")
    return {"status": True , "result": result}
