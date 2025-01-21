from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
import os
from twilio.rest import Client
from openai import OpenAI
import json
import time
from threading import Thread

app = Flask(__name__)

# Twilio credentials
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# OpenAI api key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Clients
Tclient = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
Oclient = OpenAI(api_key=OPENAI_API_KEY)

# Schedule for all reminders
schedules = []

def send_message(message, number):
    Tclient.messages.create(
        body= message, 
        from_=TWILIO_PHONE_NUMBER,
        to= f"{number}" 
    )

def add_schedule(phone_number, task, time_str, date_str):
    schedules.append({"phone": phone_number, "task": task, "time": time_str, "date": date_str})

def parse_reminder(user_message, user_number):
    parsing_response = Oclient.chat.completions.create(
        model="gpt-4o-mini",
        messages= [
            {
                "role": "developer", 
                "content": [
                    {
                        "type": "text",
                        "text": "You parse user messages into separate structured JSON response with 'task', 'time', and 'date', if provided. Ensure time is in 24 hour."
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"{user_message}"
                    }
                ]
            }
        ],
        max_tokens=100
    )
    parsed_response = parsing_response.choices[0].message.content

    parsed_data = json.loads(parsed_response)
    task = parsed_data["task"]
    date = parsed_data["date"]
    time = parsed_data["time"]

    if (task == None) | (date == None) | (time == None):
        return 0
    else:
        add_schedule(user_number, f"{task}", f"{time}", f"{date}")
    
def send_reminders():
    while True:
        for event in schedules:
            # Check if the time matches (you can improve this logic)
            if event["time"] == time.strftime("%H:%M"):
                # Create message through OpenAI api
                task = event["task"]
                number = event["phone"]
                send_message(task, number)
            print(event['phone'])
            print(event['task'])
            print(event['time'])
            print(event['date'])
        time.sleep(60)  # Check every minute

# Endpoint for creating conversation once phone number is received
conversations = {}
@app.route("/create_conversation", methods=["POST"])
def create_conversation():
    user_phone = request.json["phone_number"]
    conversation = Tclient.conversations.v1.conversations.create(
        friendly_name="New conversation"
    )
    conversations[conversation.sid] = conversation
    participant = Tclient.conversations.v1.conversations(
        conversation.sid
    ).participants.create(
        messaging_binding_address="",
        messaging_binding_proxy_address=TWILIO_PHONE_NUMBER
    )

    # Send initial message
    message = Tclient.conversations.v1.conversations(
        conversation.sid
    ).messages.create(
        body=""
    )

@app.route("/sms", methods=["POST", "GET"])
def sms_reply():
    """Respond to incoming SMS with a custom message."""
    # Get the message from the incoming request
    from_number = request.form.get("From")  # Sender's phone number
    user_message = request.form.get("Body")        # Message body
    print(f"Received message from {from_number}: {user_message}")

    # Stores reminder information 
    i = parse_reminder(user_message, from_number)
    response = MessagingResponse()

    if i == 0:
        response.message("Please be more specific in you reminder request")
    else: 
        print(f"Reminder stored: {schedules}")
        # Create a response message to send back to the user
        message = Oclient.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "developer", 
                    "content": [
                        {
                            "type": "text",
                            "text": "You create automatic responses to confirm users' reminder requests"
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"{user_message}"
                        }
                    ]
                }
            ]
        )
        message_final = message.choices[0].message.content
        response.message(message_final)

    return str(response)

# Start reminder thread
reminder_thread = Thread(target=send_reminders, daemon=True)
reminder_thread.start()

if __name__ == "__main__":
    app.run(debug=True)
