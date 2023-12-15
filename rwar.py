from tasks import add
from test import celery_app

if __name__ == '__main__':
    result = add.delay(4, 4)
    print(f'Task ID: {result.id}')
    # result.ready()
    try:
        # This will block until the result is ready or until the timeout is reached
        result_value = result.get(timeout=10)

        print(f'Result: {result_value}')
    except Exception as e:
        print(f'Error getting result: {e}')

    if result.ready():
        print('Task is ready')
    else:
        print('Task is not ready yet')
