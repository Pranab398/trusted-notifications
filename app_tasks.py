# tasks.py
import time
from celery import Celery
from config import EVENT_CONFIG, SIMULATE_PUSH_FAILURE

# Configure Celery to talk to Redis
app = Celery('notifications', broker='redis://localhost:6379/0')

@app.task(bind=True)
def send_notification_task(self, user_id, event_type, content, current_channel_index=0):
    
    # 1. Get the rules for this event
    rules = EVENT_CONFIG.get(event_type)
    channels = rules['channels']
    
    # 2. Check if we ran out of options
    if current_channel_index >= len(channels):
        print(f"❌ [CRITICAL] All channels failed for User: {user_id}")
        return "ALL_FAILED"

    current_channel = channels[current_channel_index]
    print(f"🔄 Processing Event: {event_type} | Trying Channel: {current_channel}...")

    try:
        # 3. Simulate sending to a provider
        success = mock_send_provider(current_channel, user_id, content)
        
        if success:
            print(f"✅ SUCCESS! Message delivered via {current_channel}")
            return f"SENT_{current_channel}"
        else:
            raise Exception("Simulated Provider Failure")

    except Exception as e:
        print(f"⚠️ FAILURE on {current_channel}. Initializing Smart Fallback...")
        
        # 4. THE SMART RETRY (Recursive Call)
        # Try the next channel in the list
        self.retry(
            exc=e, 
            countdown=2, # Wait 2 seconds before retrying
            args=[user_id, event_type, content, current_channel_index + 1],
            max_retries=len(channels)
        )

def mock_send_provider(channel, user_id, content):
    """
    Fake Provider. 
    Returns False if channel is PUSH (to test retry).
    Returns True for SMS.
    """
    time.sleep(1) # Fake network delay
    
    if channel == "PUSH" and SIMULATE_PUSH_FAILURE:
        return False # Fail!
        
    return True # Succeed!