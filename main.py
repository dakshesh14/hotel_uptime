import sys

import uvicorn

from fastapi import FastAPI

from api.v1.main import router as v1_router

app = FastAPI()

app.include_router(v1_router, prefix="/api/v1")


if __name__ == "__main__":

    if len(sys.argv) > 1 and sys.argv[1] == "db":
        from db.hydrate import main

        print("Hydrating DB...")
        main()
        print("Done!")

    else:
        uvicorn.run("main:app", host="localhost", port=8000, reload=True)
