import uuid

from datetime import datetime, timedelta

from fastapi import APIRouter

import asyncio

import pytz
import pandas as pd

from api.v1.models import Report, StoreReport
from db.mongo import (
    store_collection,
    menu_hour_collection,
    bq_collection,
    report_collection,
)

router = APIRouter()


store_data = pd.DataFrame(list(store_collection.find()))

if not store_data.empty:
    store_data = store_data.set_index('date')


# hard-coded date for development
# 2023-01-22 12:09:39.388884

starting_interval = datetime(2023, 1, 1, 0, 0, 0)
ending_interval = starting_interval + timedelta(hours=1)
ending_interval_in_week = starting_interval + timedelta(days=7)


@router.get("/trigger_report")
async def trigger_report():
    stores = store_collection.distinct("store_id")[0:10]

    report_id = str(uuid.uuid4())

    report = Report(
        report_id=report_id,
        store_reports=list()
    )

    report_collection.insert_one(report.dict())

    asyncio.create_task(get_uptime_downtime(stores, report))

    return report


@router.get("/get_report/{report_id}")
async def get_report(report_id: str):
    report = report_collection.find_one({"report_id": report_id})

    if report is None:
        return {"message": "report not found"}

    report = {
        **report,
        "report_id": str(report["report_id"]),
        "_id": str(report["_id"])
    }
    return report


async def get_uptime_downtime(stores, report):

    response = list()

    for store in stores:

        store_detail = store_data[store_data['store_id'] == store]

        timezone = bq_collection.find_one({"store_id": store})

        if timezone is None:
            timezone = 'America/Chicago'
        else:
            timezone = timezone['timezone']

        # TODO: don't assume the date is in UTC
        store_detail = store_detail.tz_localize('UTC').tz_convert(timezone)

        store_working_hours = menu_hour_collection.find_one(
            {"store_id": store}
        )

        if store_working_hours is None:
            start_time = '00:00'
            end_time = '23:59'
        else:
            start_time = store_working_hours['start_time_local']
            end_time = store_working_hours['end_time_local']

        business_hours = store_detail.between_time(start_time, end_time)

        # for duplicate entries
        business_hours = business_hours[
            ~business_hours.index.duplicated(keep='first')
        ]

        resampled_data = business_hours.resample('1T').ffill()

        uptime = resampled_data['status'].eq(1).astype(int)
        downtime = resampled_data['status'].eq(0).astype(int)

        uptime = uptime.resample('1T').mean()
        downtime = downtime.resample('1T').mean()

        # interpolation
        uptime = uptime.interpolate(method='linear')
        downtime = downtime.interpolate(method='linear')

        timezone = pytz.timezone(timezone)

        total_uptime = uptime.sum()
        total_downtime = downtime.sum()

        total_uptime_in_hours = round(total_uptime / 60, 2)
        total_downtime_in_hours = round(total_downtime / 60, 2)

        # TODO: for dates don't use 1T, use 1H
        total_uptime_in_last_days = round(total_uptime_in_hours * 24, 2)
        total_downtime_in_last_days = round(total_downtime_in_hours * 24, 2)

        response.append({
            "store_id": store,
            "uptime_last_hour": total_uptime_in_hours,
            "uptime_last_day": total_uptime_in_last_days,
            "download_last_hour": total_downtime_in_hours,
            "download_last_day": total_downtime_in_last_days,
        })

    report.status = "completed"
    report.store_reports = [
        StoreReport(**store_report) for store_report in response
    ]

    report_collection.update_one(
        {"report_id": report.report_id},
        {"$set": report.dict()}
    )
