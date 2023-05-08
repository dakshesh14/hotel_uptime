store_schema = {
    "store_id": {"type": "string"},
    "status": {
        "type": "integer",
        "allowed": [0, 1],
    },
    "timestamp": {"type": "datetime"},
}

menu_hour_schema = {
    "store_id": {"type": "string"},
    "start_time": {"type": "datetime"},
    "end_time": {"type": "datetime"},
    "day": {
        "type": "string",
        "allowed": [0, 1, 2, 3, 4, 5, 6],
    },
}

bq_schema = {
    "store_id": {"type": "string"},
    "timezone": {
        "type": "string",
        "default": "America/Chicago",
    },
}


report_schema = {
    "report_id": {"type": "string"},
    "store_id": {"type": "string"},
    "uptime_last_hour": {"type": "float"},
    "uptime_last_day": {"type": "float"},
    "uptime_last_week": {"type": "float"},
    "download_last_hour": {"type": "float"},
    "download_last_day": {"type": "float"},
    "download_last_week": {"type": "float"},
}
