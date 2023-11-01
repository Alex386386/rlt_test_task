import calendar
from datetime import datetime, timedelta
from typing import Dict, List, Union

from pymongo import MongoClient

from utils import mongo_host, mongo_port


def fill_gaps(data: Dict[str, Union[List[str], List[int]]],
              group_type: str,
              dt_from: str,
              dt_upto: str) -> Dict[str, List[Union[str, int]]]:
    new_dataset = []
    new_labels = []

    dt_from = datetime.fromisoformat(dt_from)
    dt_upto = datetime.fromisoformat(dt_upto)
    increments = {"hour": timedelta(hours=1),
                  "day": timedelta(days=1),
                  "month": None}

    current = dt_from
    while current <= dt_upto:
        if group_type == "month":
            label = current.replace(day=1).isoformat()
            days_in_month = calendar.monthrange(current.year, current.month)[1]
            current += timedelta(days=days_in_month)
        else:
            label = current.isoformat()
            current += increments[group_type]

        new_labels.append(label)
        if label in data["labels"]:
            index = data["labels"].index(label)
            new_dataset.append(data["dataset"][index])
        else:
            new_dataset.append(0)

    return {"dataset": new_dataset, "labels": new_labels}


def aggregate_payments(data: Dict[str, str]) -> Dict[str, List[Union[str, int]]]:
    client = MongoClient(mongo_host, mongo_port)
    db = client.sampleDB
    collection = db.sample_collection

    dt_from = datetime.fromisoformat(data["dt_from"])
    dt_upto = datetime.fromisoformat(data["dt_upto"])
    group_type = data["group_type"]

    groupings = {
        "hour": {
            "year": {"$year": "$dt"},
            "month": {"$month": "$dt"},
            "day": {"$dayOfMonth": "$dt"},
            "hour": {"$hour": "$dt"}
        },
        "day": {
            "year": {"$year": "$dt"},
            "month": {"$month": "$dt"},
            "day": {"$dayOfMonth": "$dt"}
        },
        "month": {
            "year": {"$year": "$dt"},
            "month": {"$month": "$dt"}
        }
    }

    pipeline = [
        {"$match": {"dt": {"$gte": dt_from, "$lte": dt_upto}}},
        {"$group": {
            "_id": groupings[group_type],
            "total": {"$sum": "$value"}
        }}
    ]

    results = collection.aggregate(pipeline)

    dataset = []
    labels = []
    for result in results:
        label_constructors = {
            "hour": lambda x: datetime(x["_id"]["year"], x["_id"]["month"], x["_id"]["day"],
                                       x["_id"]["hour"]).isoformat(),
            "day": lambda x: datetime(x["_id"]["year"], x["_id"]["month"], x["_id"]["day"]).isoformat(),
            "month": lambda x: datetime(x["_id"]["year"], x["_id"]["month"], 1).isoformat()
        }

        label = label_constructors[group_type](result)
        labels.append(label)
        dataset.append(result["total"])

    answer = {"dataset": dataset, "labels": labels}
    return fill_gaps(answer, group_type, data["dt_from"], data["dt_upto"])
