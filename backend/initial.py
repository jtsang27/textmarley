from flask import Flask, request, jsonify
from twilio.rest import Client
from openai import OpenAI
import os 

app = Flask(__name__)

# Twilio credentials
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize Twilio client
Tclient = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# Initialize OpenAI client
Oclient = OpenAI(api_key=OPENAI_API_KEY)

def send_initial_message(message, phone):
    Tclient.messages.create(
        body = message,
        from_ = TWILIO_PHONE_NUMBER,
        to = phone
    )

def create_response():
    message = Oclient.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "developer", 
                "content": [
                    {
                        "type": "text",
                        "text": "You create automatic responses to welcome users to a virtual assistant"
                    }
                ]
            },
        ]
    )
    return message.choices[0].message.content

@app.route("/initial", methods = ["POST"])
def initial():
    while True: 
        data = request.json
        user_phone = data["phone"]

        response = create_response()

        send_initial_message(response, user_phone)

        return f"{response} sent to {user_phone}"

if __name__ == "__main__":
    app.run(debug=True)