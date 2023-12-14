from celery_app.musicgen_tasks import add
if __name__ == '__main__':
    result = add.delay(4, 4)

    print(result)