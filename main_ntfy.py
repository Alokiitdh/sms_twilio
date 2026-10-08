import requests
import os
from dotenv import load_dotenv

load_dotenv()
TOPIC = os.getenv("NTFY_TOPIC")
## Basic messaging :- 
# requests.post("https://ntfy.sh/{TOPIC}", 
#     data="Backup successful 😀".encode(encoding='utf-8'))


## Topic based messaging with inside material
requests.post(f"https://ntfy.sh/{TOPIC}",
    data="Remote access to asus-expert-laptop detected. Act right away.",
    headers={
        "Title": "Unauthorized eeeee  access detected !!",
        "Priority": "urgent",
        "Tags": "warning,skull"
    })