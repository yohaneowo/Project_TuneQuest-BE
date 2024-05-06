from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pymongo

import os
import time

class MongoDBHandler:
    def __init__(self, uri, database_name, collection_name):
        self.client = pymongo.MongoClient(os.getenv("MONGO_URL"))
        self.db = self.client.mydatabase
        self.collection = self.db.embedded_music


    def remove_document(self, file_name):
        result = self.collection.delete_one({"file_name": {"$regex": f".*{file_name}$"}})
        if result.deleted_count > 0:
            print(f"Removed document related to {file_name} from MongoDB.")
        else:
            print(f"No document found for {file_name}.")

class MyHandler(FileSystemEventHandler):
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def on_deleted(self, event):
        if not event.is_directory:
            file_name = os.path.basename(event.src_path)
            print(f"Detected deletion: {file_name}")
            self.db_handler.remove_document(file_name)

def start_watching(path, mongo_uri, database_name, collection_name):
    db_handler = MongoDBHandler(mongo_uri, database_name, collection_name)
    event_handler = MyHandler(db_handler)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    return observer
