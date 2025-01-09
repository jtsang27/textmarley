from flask import Flask, request, jsonify
from twilio.rest import Client
from openai import OpenAI

app = Flask(__name__)

# Twilio credentials
TWILIO_SID = "ACd1fc272aaed14e7c30cec526df3fab44"
TWILIO_AUTH_TOKEN = "40694f46107d8660aabdbf1ebf63d089"
TWILIO_PHONE_NUMBER = "+18444406910"

# OpenAI API key
OPENAI_API_KEY = "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"

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