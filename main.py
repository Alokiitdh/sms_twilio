import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

message = client.messages.create(
    to="",
    from_="+17372508034",
    body="sms_delivery_updates", # here u have to choose the body based on what twilio provides
)
print(message.sid)