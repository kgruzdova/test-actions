from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

@app.get("/time")
async def get_current_time():
    """Returns the current server time in ISO 8601 format."""
    # Using datetime.now() for simplicity, this reflects the time of the machine running the server.
    current_time_iso = datetime.now().isoformat()
    return {"current_time": current_time_iso}

@app.get("/")
async def read_root():
    return {"message": "Time service is running. Use /time to get the current server time."}