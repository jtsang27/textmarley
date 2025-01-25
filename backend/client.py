from flask import Flask, request, jsonify
from twilio.rest import Client
from openai import OpenAI
import schedule
import time
from threading import Thread
import json
import os

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

Tclient = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
Oclient = OpenAI(api_key=OPENAI_API_KEY)

def intent(user_message):
    parsing_response = Oclient.chat.completions.create(
        model="gpt-4o-mini",
        messages= [
            {
                "role": "developer", 
                "content": [
                    {
                        "type": "text",
                        "text": """You parse user messages into the following actions:
                                    1. If the message asks to set a reminder, extract the task, time, and date.
                                    2. If the message asks to delete a reminder, extract the task to be deleted.
                                    3. If the message asks to edit a reminder, extract the task to be updated and the new task/time/date.
                                    4. If the message asks to list current reminders, determine if there is a time frame (e.g., "today", "this week").

                                    Parse task, time, and date into separate structured JSON response. Translate time to 24 hour.
                                """
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

    return parsed_response


message = "Delete my reminder at 8 pm"

print(intent(message))