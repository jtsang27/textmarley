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

Tclient.conversations.v1.conversations(
    "CH79cf33aa952b405d8ec84a7d0676bb92"
).delete()

"""
# Create assistant 
Assistant = Oclient.beta.assistants.create(
    name="Marley", 
    instructions="You are a friendly personal assistant that help set reminders and centralize deadlines lists.",
    model="gpt-4o-mini", 
    temperature=1.0,
    top_p=1.0,
    tools=[]
)

# Create thread
thread = Oclient.beta.threads.create()

# Create and append message to thread
message = Oclient.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Set a reminder for my math homework tonight at 6 pm"
)

# Run agent on thread
run = Oclient.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=Assistant.id,
)

if run.status == 'completed': 
    messages = Oclient.beta.threads.messages.list(
    thread_id=thread.id, order="desc", limit=3
    )
    print(messages.data[0].content[0].text.value) # Get the latest message
else:
    print(run.status)

def send_message():
    Tclient.messages.create(
        body= "hello jonathan", 
        from_=TWILIO_PHONE_NUMBER,
        to= "2063343224" 
    )
#send_message()
user_message = "Set me a reminder for my math homework at 5 45 today"

message = Tclient.conversations.v1.conversations(
    "CH5bde8f09d4184ebbb81f27e4aba438bb"
).messages.create(
    author="smee",
    body="Testing"
)

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
"""