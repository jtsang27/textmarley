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
                        "text": """You categorize user intent into the following actions:
                                    0. Message asks to set a reminder
                                    1. Message asks to delete a reminder
                                    2. Message asks to edit a reminder
                                    3. Message asks to list current reminders
                                    4. Other

                                    Return number associated with action
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

def parse_set(user_message):
    parsing_response = Oclient.chat.completions.create(
        model="gpt-4o-mini",
        messages= [
            {
                "role": "developer", 
                "content": [
                    {
                        "type": "text",
                        "text": "You parse user messages into separate structured JSON response with 'task', 'time', and 'date', if provided. Translate time to 24 hour."
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

def parse_delete(user_message):
    parsing_response = Oclient.chat.completions.create(
        model="gpt-4o-mini",
        messages= [
            {
                "role": "developer", 
                "content": [
                    {
                        "type": "text",
                        "text": "You parse user messages into separate structured JSON response with 'task', 'time', and 'date', if provided. Translate time to 24 hour."
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

def parse_edit(user_message):
    parsing_response = Oclient.chat.completions.create(
        model="gpt-4o-mini",
        messages= [
            {
                "role": "developer", 
                "content": [
                    {
                        "type": "text",
                        "text": "You parse user messages into separate structured JSON response with 'task', 'time', and 'date', if provided. Translate time to 24 hour."
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

def parse_list(user_message):
    parsing_response = Oclient.chat.completions.create(
        model="gpt-4o-mini",
        messages= [
            {
                "role": "developer", 
                "content": [
                    {
                        "type": "text",
                        "text": """You parse user messages into separate structured JSON response with 'time frame' and 'date', if provided. 
                                    If not provided, assume 'date' is today and 'time frame' is null"""
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

message = "remind me to take notes for my meeting at 9am"

print(intent(message))