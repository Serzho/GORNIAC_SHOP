import uvicorn
import sys

sys.path.append("../../../backend")
from cfg import HOST_API, PORT_API
from core.sevice import mount_static_files
from endpoints.endpoints import app

mount_static_files(app)

if __name__ == "__main__":
    uvicorn.run(app=app, host=HOST_API, port=PORT_API)
