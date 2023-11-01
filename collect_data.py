import json
from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId

from utils import mongo_host, mongo_port


def connect_to_mongo(host, port):
    client = MongoClient(host, port)
    return client.sampleDB.sample_collection


def transform_document(doc):
    doc["_id"] = ObjectId(doc["_id"]["$oid"])
    doc["dt"] = datetime.utcfromtimestamp(int(doc["dt"]["$date"]["$numberLong"]) / 1000)
    doc["value"] = int(doc["value"]["$numberInt"])
    return doc


def main():
    collection = connect_to_mongo(mongo_host, mongo_port)

    with open("output.json", "r") as f:
        lines = f.readlines()

    documents = [transform_document(json.loads(line)) for line in lines]
    collection.insert_many(documents)


if __name__ == "__main__":
    main()
