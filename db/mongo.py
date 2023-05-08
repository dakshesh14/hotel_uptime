from pymongo import MongoClient

from .schema import (
    store_schema,
    menu_hour_schema,
    bq_schema,
    report_schema,
)

# TODO: use env variable
MONGO_URI = "mongodb://localhost:27017"

client = MongoClient(MONGO_URI)

db = client.get_default_database("store_status")


store_collection = db.get_collection("store_status")
if store_collection is None:
    store_collection = db.create_collection(
        "store_status",
        validator=store_schema
    )

menu_hour_collection = db.get_collection("menu_hour")
if menu_hour_collection is None:
    menu_hour_collection = db.create_collection(
        "menu_hour",
        validator=menu_hour_schema
    )

bq_collection = db.get_collection("bq_results")
if bq_collection is None:
    bq_collection = db.create_collection(
        "bq_results",
        validator=bq_schema
    )

report_collection = db.get_collection("reports")
if report_collection is None:
    report_collection = db.create_collection(
        "reports",
        validator=report_schema
    )
