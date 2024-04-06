from celery_app.musicgen_tasks import generate_music

from celery.result import AsyncResult
if __name__ == '__main__':
    result = generate_music.delay()
    # result2 = add.delay()

    # 使用 AsyncResult 等待任務完成
    result_instance = AsyncResult(result.id)
    # result_instance2 = AsyncResult(result2.id)

    try:
        # 等待並取得結果
        result_value = result_instance.get()
        # result_value2 = result_instance2.get()
        print(f'Result 1: {result_value}')
        # print(f'Result 2: {result_value2}')

    except Exception as e:
        print(f'Error getting result: {e}')

    if result_instance.ready():
        print('Task 1 is ready')
    else:
        print('Task 1 is not ready yet')
    #
    # if result_instance2.ready():
    #     print('Task 2 is ready')
    # else:
    #     print('Task 2 is not ready yet')