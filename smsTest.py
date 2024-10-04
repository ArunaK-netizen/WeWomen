from twilio.rest import Client
import os
from dotenv import load_dotenv
# Twilio account details
load_dotenv()
account_sid = os.getenv('account_sid')
auth_token = os.getenv('auth_token')
client = Client(account_sid, auth_token)
def send_message(phone_number, message):
    client.messages.create(
        body=message,
        from_='+16318498574',
        to=phone_number
    )

if __name__ == "__main__":
    phone_number = '+917397599719'  # receiver's number in international format
    message = "Hello, this is a test message."
    send_message(phone_number, message)
