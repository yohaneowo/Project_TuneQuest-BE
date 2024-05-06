from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from fastapi.responses import JSONResponse
from src.music_genre_classification.classification_core import predict_genre
from src.sematic_search.sematic_search_core import create_item as create_sematic_search_item , GeneratedMusic
from celery_app.musicgen_tasks import generate_music
import os
import shutil
from datetime import datetime
from celery.result import AsyncResult
from fastapi.responses import FileResponse
from pymongo import MongoClient
from bson.json_util import dumps, loads
import requests
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
import uuid

router = APIRouter(
    prefix='/musicgen_generate_music',
    tags=['musicgen_generate_music']
)

@router.get('/music_storage/all')
async def get_all_music_files():
    # Requires the PyMongo package.
    # https://api.mongodb.com/python/current
    try:

        client = MongoClient(
            'mongodb+srv://admin_2:a5o846aS6bLN091e@cluster0.ousfkbb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
        filter = {}
        project = {"_id":0, "embedded_prompt":0, "embedded_audio":0}
        sort = list({}.items())
        collation = {}

        cursor = client['mydatabase']['embedded_music'].find(
            filter=filter,
            projection=project,
            sort=sort,
            collation=collation
        )
        list_cur = list(cursor)
        return list_cur
    except Exception as e:
        print(f'An error occurred: {e}')

@router.get('/music_storage/{file_name}')
async def get_music_file(file_name: str):
    folder_path = os.path.join(os.getcwd(), "music_storage")
    file_path = os.path.join(folder_path, file_name)
    check_file = os.path.isfile(file_path)
    if check_file:
        print("music file exist")
        return FileResponse(path=file_path, filename=file_name)
    else:
        return "file not exist"

@router.post("/music_storage/album/upload/")
async def upload_file(file: UploadFile = File(...)):
    # 设置文件保存路径为当前工作目录下的 music_storage 文件夹
    save_path = os.path.join(os.getcwd(), "music_storage", "album")
    try:
        # 创建保存路径的文件夹如果它还不存在
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # 保存文件
        file_path = os.path.join(save_path, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        relative_path = os.path.join("music_storage", "album", file.filename)
        return JSONResponse(content={"message": "File uploaded successfully", "file_path": relative_path})
    except Exception as e:
        return JSONResponse(content={"message": f"Failed to upload album file: {str(e)}"}, status_code=500)

@router.post("/music_storage/rename/")
async def rename_file(old_file_name: str, prompt: str):
    # 设置文件保存路径为当前工作目录下的 music_storage 文件夹
    print("im here")
    save_path = os.path.join(os.getcwd(), "music_storage")
    file_path = os.path.join(save_path, old_file_name)
    new_file_name = f"{prompt}_{old_file_name}"
    new_file_path = os.path.join(save_path, new_file_name)
    relative_path = os.path.join("music_storage", new_file_name)
    try:
        # 检查原始文件是否存在
        if not os.path.isfile(file_path):
            return JSONResponse(content={"message": "File not found"}, status_code=404)

        # 检查新文件名是否已经存在
        if os.path.exists(new_file_path):
            return JSONResponse(content={"message": "New file name already exists"}, status_code=400)

        # 重命名文件
        os.rename(file_path, new_file_path)

        return JSONResponse(content={"message": "File renamed successfully", "new_file_name": new_file_name, "new_file_path":relative_path}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": f"Failed to rename file: {str(e)}"}, status_code=500)
@router.post("/music_storage/upload/")
async def upload_file( file: UploadFile = File(...)):
    # 设置文件保存路径为当前工作目录下的 music_storage 文件夹

    save_path = os.path.join(os.getcwd(), "music_storage")
    try:
        # 创建保存路径的文件夹如果它还不存在
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        unique_id = uuid.uuid4()

        uuid_filename = f"{unique_id}.wav"
        # 保存文件
        file_path = os.path.join(save_path,uuid_filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        relative_path = os.path.join("music_storage", uuid_filename)

        return JSONResponse(content={"message": "File uploaded successfully", "file_path": relative_path, "file_name": uuid_filename})
    except Exception as e:
        return JSONResponse(content={"message": f"Failed to upload file: {str(e)}"}, status_code=500)

@router.post('/musicgen')
async def musicgen_generate_music(prompt: str, duration: int ):
    result =  generate_music.delay(prompt, duration)
    # result2 = add.delay()
    print("test")
    # 使用 AsyncResult 等待任務完成
    print(result)
    result_instance = AsyncResult(result.id)
    # result_instance2 = AsyncResult(result2.id)

    try:
        # 等待並取得結果
        result_value = result_instance.get()
        print(result_value)
        print(f'Result 1: {result_value}')
        audiofile_path = result_value['result']['audiofile_path']
        audiofile_name = result_value['result']['audiofile_name']
        genre = await request_music_genre_classification(audiofile_path)
        # print(genre)
        create_sematic_search_item_result = await create_sematic_search_data(genre, prompt, audiofile_path, audiofile_name, duration)
        audio_info = {
            "audiofile_name" : audiofile_name,
            "audiofile_path": audiofile_path,
            "genre": genre,
            "prompt": prompt,
            "duration": duration,
        }
        return audio_info
        # print(create_sematic_search_item_result)

    except Exception as e:
        print(f'Error getting result: {e}')

    if result_instance.ready():
        print('Task 1 is ready')
    else:
        print('Task 1 is not ready yet')


@router.post("/music_storage/uploadTempMusic_to_classification/")
async def upload_file(file: UploadFile = File(...)):
    # 设置文件保存路径为当前工作目录下的 music_storage 文件夹

    save_path = os.path.join(os.getcwd(), "music_storage", "temp")
    try:
        # 创建保存路径的文件夹如果它还不存在
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # 保存文件到指定路径
        file_path = os.path.join(save_path, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 生成相对路径
        relative_path = os.path.join("music_storage", "temp", file.filename)

        # 对文件执行一些操作（假设是处理函数）
        genre = await request_music_genre_classification(file_path)
        return JSONResponse(content={"message": "File processed and deleted successfully", "file_path": relative_path, "genre":genre, "file_name": file.filename})

        # 处理完后删除文件
        # os.remove(file_path)


    except Exception as e:
        # 如果处理或删除时出现错误，尝试删除文件
        if os.path.exists(file_path):
            os.remove(file_path)
        return JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR, content={"message": f"Failed to process and delete file: {str(e)}"})

async def request_music_genre_classification(relative_filePath:str):
    url = "http://127.0.0.1:9988/music_genre_classification/predict"
    file_path = os.path.join(os.getcwd(), relative_filePath)
    check_file = os.path.isfile(file_path)
    if check_file:
        print("music file exist")
        print("Start music file classification")
    try:
        # Open the file in binary mode and prepare the request
        print("ok?")
        predict_genre_result = predict_genre(file_path)
        # print(predict_genre_result)
        return predict_genre_result['genre']
        # with open(file_path, 'rb') as file:
        #     contents = await file.read()
        #     upload_file = UploadFile(filename=file_path, file=io.BytesIO(contents))
        #     result = predict_genre(upload_file)
        #     print(result)
        #     print("ok ??? result    ")
            # files = {'file': file}
            # print(files)
            # print("ok2")
            # response = requests.post(url, files=files)
            # print(response)
            # print("ok3")
            # Check the response status code
            # if response.status_code == 200:
            #     # Request was successful
            #     print("Prediction successful!")
            #     print("Predicted genre:", response.json())
            # elif response.status_code == 422:
            #     # Validation error
            #     print("Validation Error:", response.json())
            # else:
            #     # Other errors
            #     print("Error:", response.status_code)

    except Exception as e:
        # Catch any exceptions that occur
        print("An error occurred during classification:", e)
@router.post("/create_semantic_search_data/")
async def create_semantic_search_data_api(genre:str,prompt:str,audiofile_path:str, audiofile_name:str, duration:int):

    try:
        response = await create_sematic_search_data(genre, prompt, audiofile_path, audiofile_name, duration)
        return response
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

async def create_sematic_search_data(genre:str,prompt:str,audiofile_path:str, audiofile_name:str, duration:int):
    music_data = GeneratedMusic(
        name=prompt,
        genre=genre,
        prompt=prompt,
        user_id=123,
        file_name=audiofile_name,
        created_at=get_current_utc_time_iso(),
        store_path=audiofile_path,
        duration=duration,
        embedded_prompt=[0],
        embedded_audio=[0]
    )
    print(music_data)

    try:
        response = await create_sematic_search_item(music_data)
        print(response)
        return response
    except Exception as e:
        # Catch any exceptions that occur
        print("An error occurred during sematic_search_creation:", e)


# async def create_sematic_search_data( genre: str, prompt: str, audiofile_path: str):
#     url = "http://127.0.0.1:9988/sematic_search/items/"
#
#     # 获取当前时间并格式化为字符串
#     created_at = datetime.now().isoformat()
#
#     payload = {
#         "name": "Midnight Jazz Escape",  # 这个名称是硬编码的，你可能需要根据情况修改
#         "genre": genre,
#         "prompt": prompt,
#         "user_id": 123,  # 这个用户 ID 也是硬编码的，你可能需要根据情况修改
#         "created_at": created_at,  # 使用当前时间作为创建时间
#         "store_path": audiofile_path,
#         "embedded_prompt": [0],  # 这个也是硬编码的，你可能需要根据情况修改
#         "embedded_audio": [0]    # 同上
#     }
#
#     headers = {
#         "Content-Type": "application/json"
#     }
#
#     try:
#         print("not again?")
#         response = requests.post(url, json=payload, headers=headers)
#         print("not again?2")
#
#         response.raise_for_status()  # 抛出异常如果请求失败
#         print("Item created successfully!")
#         return response  # 返回响应对象
#     except requests.exceptions.HTTPError as err:
#         print("HTTP error occurred:", err)
#     except requests.exceptions.RequestException as err:
#         print("An error occurred:", err)
#
def get_current_utc_time_iso():
    # 获取当前 UTC 时间，并格式化为ISO 8601格式，包括毫秒和'Z'
    return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'