from flask import Flask, request, jsonify
from twilio.rest import Client
from openai import OpenAI
import schedule
import time
from threading import Thread

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
user_message = "Send me 2 reminders before my exam on Friday at 9 am."


parsing_response = Oclient.chat.completions.create(
    model="gpt-4o-mini",
    messages= [
        {
            "role": "developer", 
            "content": [
                {
                    "type": "text",
                    "text": "You parse user messages into separate structured JSON response with 'task', 'time', and 'date'."
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
parsed_data = eval(parsed_response) # readable by user 

task = parsed_data["task"]
date = parsed_data["date"]
time_ = parsed_data["time"]

print(task, date, time_)
