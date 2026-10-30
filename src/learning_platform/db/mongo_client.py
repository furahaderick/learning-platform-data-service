from pymongo import MongoClient

from learning_platform.config import mongo_settings


def create_mongo_database():
    settings = mongo_settings()
    client = MongoClient(settings["uri"])
    return client, client[settings["database"]]
