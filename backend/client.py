from flask import Flask, request, jsonify
from twilio.rest import Client
from openai import OpenAI
import schedule
import time
from threading import Thread
import json

TWILIO_SID = "ACd1fc272aaed14e7c30cec526df3fab44"
TWILIO_AUTH_TOKEN = "40694f46107d8660aabdbf1ebf63d089"
TWILIO_PHONE_NUMBER = "+18444406910"

OPENAI_API_KEY = "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"

Tclient = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
Oclient = OpenAI(api_key=OPENAI_API_KEY)

def send_message():
    Tclient.messages.create(
        body= "hello jonathan", 
        from_=TWILIO_PHONE_NUMBER,
        to= "2063343224" 
    )
#send_message()
user_message = "Set me a reminder for my math homework at 4:20 pm today"


parsing_response = Oclient.chat.completions.create(
    model="gpt-4o-mini",
    messages= [
        {
            "role": "developer", 
            "content": [
                {
                    "type": "text",
                    "text": "You parse user messages into separate structured JSON response with 'task', 'time', and 'date', if provided."
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
#print(parsed_response)

parsed_data = json.loads(parsed_response)
print(f"reminder: {parsed_data}")

task = parsed_data["task"]
date = parsed_data["date"]
time_ = parsed_data["time"]

schedules = []

def add_schedule(phone_number, task, time_str, date_str):
    schedules.append({"phone": phone_number, "task": task, "time": time_str, "date": date_str})

if (task == None) | (date == None) | (time_ == None):
    print(0)
else:
    add_schedule("2063343224", f"{task}", f"{time_}", f"{date}")

print(schedules)
for event in schedules:
    print(event['phone'])
    print(event['task'])
    print(event['time'])
    print(event['date'])

for event in schedules:
    # Check if the time matches (you can improve this logic)
        if event["time"] == time.strftime("%H:%M"):
            # Create message through OpenAI api
            task = event["task"]
            number = event["phone"]
            """
            Tclient.messages.create(
                body= event["message"],
                from_=TWILIO_PHONE_NUMBER,
                to= event["phone"]
            )
            """
            send_message()

