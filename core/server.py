import uvicorn
from cfg import HOST_API, PORT_API
from core.service import mount_static_files, base_logger
from core.endpoints.endpoints import app
from core.image_updater import update_images


def log(message: str) -> None:
    module_name = "SERVER"
    base_logger(msg=message, module_name=module_name)


if __name__ == "__main__":
    mount_static_files(app)
    update_images()
    log("Static files mounted")
    log("Starting uvicorn server...")
    uvicorn.run(app=app, host=HOST_API, port=PORT_API)
    log("Application shutting down...")
