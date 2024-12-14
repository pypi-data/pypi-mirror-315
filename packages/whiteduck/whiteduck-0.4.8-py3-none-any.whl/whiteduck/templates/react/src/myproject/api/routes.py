from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import platform
import psutil
import datetime

app = FastAPI()

@app.get("/api/data")
async def get_data():
    return {"message": "Hello from FastAPI!"}

@app.get("/api/system_info")
async def get_system_info():
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    return {
        "os": {
            "name": platform.system(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor()
        },
        "memory": {
            "total": f"{psutil.virtual_memory().total / (1024 * 1024 * 1024):.2f} GB",
            "available": f"{psutil.virtual_memory().available / (1024 * 1024 * 1024):.2f} GB",
            "percent_used": psutil.virtual_memory().percent
        },
        "cpu": {
            "cores": psutil.cpu_count(),
            "physical_cores": psutil.cpu_count(logical=False),
            "current_frequency": f"{psutil.cpu_freq().current:.2f} MHz",
            "usage_percent": psutil.cpu_percent(interval=1)
        },
        "system": {
            "boot_time": boot_time,
            "python_version": platform.python_version()
        }
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the current file's directory
current_dir = Path(__file__).parent.parent.parent
# Construct path to the dist directory
dist_path = current_dir / "frontend" / "dist"

# Custom StaticFiles class to set JavaScript MIME type
class SPAStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        response = await super().get_response(path, scope)
        if path.endswith('.js'):
            response.headers['Content-Type'] = 'application/javascript'
        return response

# Mount the static files with custom handler
app.mount("/", SPAStaticFiles(directory=str(dist_path), html=True), name="static")
