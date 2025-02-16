# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, DataHistory
from schemas import DeviceLog
from typing import List
from fastapi import HTTPException

# Create database tables if they don't exist yet
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Enable CORS (adjust origins as needed)
origins = ["http://localhost", "http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def parse_reading(reading: str):
    """
    Parse the sensor reading string.
    Format examples:
    1. Watering started:
       "epochtime:w1:milliseconds_elapsed:flow_reading_before_opening ~ epochtime:Battery_voltage ~"
    2. Watering stopped:
       "epochtime:w0:time_elapsed:flowreading_before_closing:milliseconds_after_closing:flowreading ~ epochtime:Battery_voltage ~"
    """
    parts = [p.strip() for p in reading.split("~") if p.strip()]
    battery_voltage = None
    watering_status = "Unknown"
    issues = ""
    
    if len(parts) >= 2:
        # Parse battery info
        battery_part = parts[1]
        tokens = battery_part.split(":")
        if len(tokens) >= 2:
            try:
                battery_voltage = float(tokens[1].strip())
            except Exception as e:
                issues += f"Battery voltage parse error: {str(e)}; "
        else:
            issues += "Battery voltage part format error; "
    
    event_part = parts[0]
    tokens = event_part.split(":")
    if len(tokens) >= 2:
        event_flag = tokens[1].strip()
        if event_flag == "w1":
            watering_status = "Watering started"
        elif event_flag == "w0":
            watering_status = "Watering stopped"
        else:
            watering_status = f"Unknown event: {event_flag}"
    else:
        issues += "Event part format error; "
    
    return watering_status, battery_voltage, issues

@app.get("/device_logs", response_model=List[DeviceLog])
def get_device_logs():
    db: Session = SessionLocal()
    try:
        logs = db.query(DataHistory).all()
        result = []
        for log in logs:
            watering_status, battery_voltage, issues = parse_reading(log.reading_string)
            result.append(DeviceLog(
                id=log.id,
                user_id=log.user_id,
                name=log.name,
                watering_status=watering_status,
                battery_voltage=battery_voltage,
                issues=issues
            ))
        return result
    finally:
        db.close()
