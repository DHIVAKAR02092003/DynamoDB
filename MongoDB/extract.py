from pymongo import MongoClient 
from configparser import ConfigParser 
from pathlib import Path 
import pandas as pd

def extract():
    config = ConfigParser()
    config.read(Path(__file__).parent.parent / "config" / "config.ini")

    uri = config["mongodb"]["URI"]
    db_name = config["mongodb"]["DB"]
    collection_name = config["mongodb"]["Collection"]

    client = MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name] 

    data = list(collection.find({}))
    result = pd.DataFrame(data)
    
    return result