import uvicorn
import sys

sys.path.append("../../../backend")

from cfg import HOST_API, PORT_API
from core.service import mount_static_files, base_logger
from endpoints.endpoints import app


def log(message: str) -> None:
    module_name = "SERVER"
    base_logger(msg=message, module_name=module_name)


if __name__ == "__main__":
    mount_static_files(app)
    log("Static files mounted")
    log("Starting uvicorn server...")
    uvicorn.run(app=app, host=HOST_API, port=PORT_API)
    log("Application shutting down...")
