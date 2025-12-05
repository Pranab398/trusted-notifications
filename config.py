# config.py

# The Logic: Try Push first. If it fails (or no Ack in 5s), try SMS.
EVENT_CONFIG = {
    "OTP_LOGIN": {
        "channels": ["PUSH", "SMS"], 
        "ack_timeout": 5 
    },
    "TRANSACTION_ALERT": {
        "channels": ["PUSH", "EMAIL"],
        "ack_timeout": 10
    }
}

# DEMO TRICK: Set this to True to prove your system fixes failures automatically
SIMULATE_PUSH_FAILURE = True