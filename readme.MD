# Hotel uptime/download calculation

Made using FastAPI and mongodb. Reason to chose mongodb is because it offers fast read speed for large data sets. I chose FastAPI because function in FastAPI are async, meaning it won't block the request thread while the interpolation is running.

## How to run

1. Clone the repo
2. Create `data` folder in the root directory with store-status.csv, menu-hours.csv, and bq-results.csv inside it.
3. Setup environment.
4. Run `python main.py db` to populate the database.
5. Run `python main.py` to start the server.

## Endpoints

### http://localhost:8000/api/v1/trigger_report

This endpoint will trigger the report generation. It will return the report id. The report will be generated in the background.

### http://localhost:8000/api/v1/get_report/{report_id}

This endpoint will return the report. If the report is not ready, it will send response with status being `running`. If the report is ready, it will send response with status being `complete` and the report data.

## How interpolation works

Interpolation basically is a way to estimate the value of a function between two known values. In this case, we had to get the store's for every interval. I am using linear interpolation to estimate the value between two known values. The formula is:

```
y = y1 + (x - x1) * ((y2 - y1) / (x2 - x1))
```

Where `x` is the time, `y` is the store's status, `x1` and `x2` is the time of the known values, `y1` and `y2` is the store's status of the known values.

## How uptime calculation works

Uptime is calculated by counting the number of `up` status in the store's status. The uptime is then divided by the total number of store's status. The formula is:

```
uptime = (up_count / total_count)
```

## Things to improve

1. Add test
2. Add more error handling
3. Cache the report data
