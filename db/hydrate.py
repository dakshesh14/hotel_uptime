import os
import csv

import pytz
from datetime import datetime

from db.mongo import (
    store_collection,
    menu_hour_collection,
    bq_collection,
)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


STORE_CSV = os.path.join(BASE_DIR, 'data', 'store-status.csv')
MENU_HOUR_CSV = os.path.join(BASE_DIR, 'data', 'menu-hours.csv')
BQ_CSV = os.path.join(BASE_DIR, 'data', 'bq-results.csv')


def load_store_status():
    with open(STORE_CSV, 'r') as file:
        reader = csv.DictReader(file)
        data = list(
            {
                **row,
                "store_id": row["store_id"],
                "status": 1 if row["status"] == "active" else 0,
                "date": datetime.strptime(row["timestamp_utc"].replace(" UTC", "").split(".")[0], "%Y-%m-%d %H:%M:%S"),
            } for row in reader
        )

    store_collection.insert_many(data)


def load_menu_hour():
    with open(MENU_HOUR_CSV, 'r') as file:
        reader = csv.DictReader(file)
        data = list(
            {
                **row,
                "store_id": row["store_id"],
                "day_of_week": int(row["day"]),
            } for row in reader
        )

    menu_hour_collection.insert_many(data)


def load_bq_results():
    with open(BQ_CSV, 'r') as file:
        reader = csv.DictReader(file)
        data = list(
            {
                **row,
                "store_id": row["store_id"],
                "timezone": row["timezone_str"] if row["timezone_str"] else "America/Chicago",
            } for row in reader
        )

    bq_collection.insert_many(data)


def main():
    load_store_status()
    load_menu_hour()
    load_bq_results()
