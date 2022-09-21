import sys

import uvicorn
from fastapi import FastAPI
sys.path.append("../../../backend")
from backend.cfg import HOST_API, PORT_API

app = FastAPI()


@app.get("/test")
async def test() -> dict:
    return {"blocks": "GAAAAAAAY"}

if __name__ == "__main__":
    uvicorn.run(app=app, host=HOST_API, port=PORT_API)

