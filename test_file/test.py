from datetime import datetime
import requests

def create_sematic_search_data():
    url = "http://127.0.0.1:9988/sematic_search/items/"


    payload = {
        "name": "Midnight Jazz Escape",
        "genre": "Jazz",
        "prompt": "Late night jazz with a melancholic piano and a double bass groove",
        "user_id": 123,
        "created_at": get_current_utc_time_iso(),
        "store_path": "./sample/tmpte4m9jx6.wav",
        "embedded_prompt": [0],
        "embedded_audio": [0]
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # 抛出异常如果请求失败
        print("Item created successfully!")
        return response.json()
    except requests.exceptions.HTTPError as err:
        print("HTTP error occurred:", err)
    except requests.exceptions.RequestException as err:
        print("An error occurred:", err)


def get_current_utc_time_iso():
    # 获取当前 UTC 时间，并格式化为ISO 8601格式，包括毫秒和'Z'
    return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

test = create_sematic_search_data()
print(test)