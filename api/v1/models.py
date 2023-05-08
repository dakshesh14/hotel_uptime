from pydantic import BaseModel


class StoreReport(BaseModel):
    store_id: str
    uptime_last_hour: float
    uptime_last_day: float
    download_last_hour: float
    download_last_day: float


class Report(BaseModel):
    report_id: str
    status: str = "running"
    store_reports: list[StoreReport]
