from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app_tasks import send_notification_task
import uuid
import time

app = FastAPI()

# Allow the browser to talk to the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# The memory database
fake_db = []

class NotificationRequest(BaseModel):
    user_id: str
    event_type: str 
    content: dict

# --- 1. SEND NOTIFICATION (Manual) ---
@app.post("/send")
def trigger_notification(request: NotificationRequest):
    request_id = str(uuid.uuid4())
    fake_db.append({
        "id": request_id,
        "user": request.user_id,
        "type": request.event_type,
        "status": "Processing...",
        "verified": True
    })
    send_notification_task.delay(request.user_id, request.event_type, request.content)
    return {"status": "Queued", "id": request_id}

# --- 2. GET NOTIFICATIONS (Frontend polling) ---
@app.get("/notifications")
def get_notifications():
    return fake_db

# --- 3. ANALYTICS (Simulated Stats for the Chart) ---
@app.get("/analytics")
def get_analytics():
    # Hardcoded stats so the Chart always works
    return [
        {"Event_Type": "OTP Login", "Retry_Percentage": 52.8},
        {"Event_Type": "Fraud Alert", "Retry_Percentage": 44.6},
        {"Event_Type": "Bill Reminder", "Retry_Percentage": 59.1},
        {"Event_Type": "KYC Update", "Retry_Percentage": 57.2}
    ]

# --- 4. BATCH SIMULATION (Hardcoded - No CSV needed) ---
def run_simulation_logic():
    print("--- SIMULATION STARTED ---")
    
    # We simulate 5 distinct events
    events = [
        {"type": "Credit Card Bill", "channel": "Push", "user": "Rohit"},
        {"type": "Large Transfer Alert", "channel": "SMS", "user": "Pranab"},
        {"type": "Login OTP", "channel": "Push", "user": "Amit"},
        {"type": "Policy Update", "channel": "Email", "user": "Sneha"},
        {"type": "Suspicious Login", "channel": "WhatsApp", "user": "Rahul"}
    ]

    for event in events:
        time.sleep(1.5) # Wait 1.5 seconds between each message
        
        # Add to the UI list
        fake_db.append({
            "id": str(uuid.uuid4()),
            "user": f"Cust_{event['user']}",
            "type": event['type'],
            "status": f"Simulated via {event['channel']}",
            "verified": True
        })
        print(f"-> Simulated: {event['type']} for {event['user']}")
        
        # Trigger the Worker
        send_notification_task.delay(
            f"Cust_{event['user']}", 
            event['type'], 
            {"message": "Batch Test"}
        )

@app.post("/simulate")
def trigger_simulation(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_simulation_logic)
    return {"message": "Batch Simulation Started"}