# Notification Service (Twilio & ntfy.sh)

A lightweight notification pipeline built in Python and managed with [`uv`](https://docs.astral.sh/uv/). It supports both telecom-based messaging (Twilio SMS/WhatsApp) and direct, registration-free push notifications to mobile or desktop devices using [ntfy.sh](https://ntfy.sh).

---

## Features

- **Push Notifications via `ntfy.sh`**: Free, open-source, instant push notifications with no carrier restrictions or account required.
- **Twilio SMS & WhatsApp**: Programmatic SMS delivery and WhatsApp messaging via Twilio REST API.
- **Fast Package Management**: Uses `uv` for dependency resolution and execution.
- **Environment Isolation**: Secure credential management using `.env`.

---

## Prerequisites

- [Python](https://www.python.org/) 3.10+
- [`uv`](https://docs.astral.sh/uv/) installed
- Mobile device with the **ntfy** app installed ([Android](https://play.google.com/store/apps/details?id=io.heckel.ntfy) / [iOS](https://apps.apple.com/app/ntfy/id1625396347)) or a browser
- (Optional) [Twilio Account](https://www.twilio.com/) credentials for SMS/WhatsApp

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/<your-username>/sms_twilio.git
   cd sms_twilio
   ```

2. **Install project dependencies:**
   ```bash
   uv add requests python-dotenv twilio
   ```

---

## Configuration

Create a `.env` file in the project root:

```env
# --- ntfy.sh Settings ---
# Pick a random, unguessable string for your topic name
NTFY_TOPIC=alok_alerts_x92k1

# --- Twilio Settings (Optional) ---
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1xxxxxxxxxx
TARGET_PHONE_NUMBER=+91xxxxxxxxxx
```

Ensure `.env` is omitted from version control:

```bash
echo ".env" >> .gitignore
```

---

## Method 1: Push Notifications via ntfy.sh (Recommended)

### 1. Subscribe to Topic
1. Open the **ntfy** mobile app (or visit `https://ntfy.sh/app`).
2. Tap **+** (Subscribe) and enter the exact topic name set in your `.env` (e.g., `alok_alerts_x92k1`).

### 2. Python Script (`send_ntfy.py`)

```python
import os
import requests
from dotenv import load_dotenv

load_dotenv()

topic = os.getenv("NTFY_TOPIC", "alok_alerts_x92k1")

response = requests.post(
    f"https://ntfy.sh/{topic}",
    data="Heyyyy it worked via ntfy!".encode("utf-8"),
    headers={
        "Title": "System Notification",
        "Priority": "urgent",       # min, low, default, high, urgent
        "Tags": "tada,rocket",      # emoji tags
    },
)

if response.status_code == 200:
    print(f"Notification delivered! (Status: {response.status_code})")
else:
    print(f"Failed to send: {response.status_code} - {response.text}")
```

### 3. Run

```bash
uv run send_ntfy.py
```

---

## Method 2: Messaging via Twilio

### SMS (`main.py`)

```python
import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

message = client.messages.create(
    to=os.environ["TARGET_PHONE_NUMBER"],
    from_=os.environ["TWILIO_PHONE_NUMBER"],
    body="Heyyyy it worked via SMS!",
)

print(f"SMS Sent! SID: {message.sid}")
```

Run:
```bash
uv run main.py
```

### WhatsApp Sandbox (`whatsapp.py`)

> Required for Twilio trial accounts sending to international numbers without registered DLT templates.

```python
import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

message = client.messages.create(
    to=f"whatsapp:{os.environ['TARGET_PHONE_NUMBER']}",
    from_="whatsapp:+14155238886",  # Twilio Sandbox number
    body="Heyyyy it worked via WhatsApp!",
)

print(f"WhatsApp Sent! SID: {message.sid}")
```

Run:
```bash
uv run whatsapp.py
```

---

## Troubleshooting

| Error | Root Cause | Fix |
|---|---|---|
| `KeyError: 'TWILIO_ACCOUNT_SID'` | Missing environment variable | Install `python-dotenv` and execute `load_dotenv()` before `os.environ`. |
| `TwilioRestException: 572006` | Trial SMS restrictions on Indian numbers (+91) | Use `ntfy.sh` for push alerts or the Twilio WhatsApp Sandbox for testing. |
| Notification not received on `ntfy` | Topic name mismatch | Confirm that the topic subscribed in the app matches `NTFY_TOPIC` in `.env`. |