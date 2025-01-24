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

