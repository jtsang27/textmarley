from flask import Flask, request, jsonify
from twilio.rest import Client
from openai import OpenAI
import schedule
import time
from threading import Thread

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

# Database to store user schedules
schedules = []

def add_schedule(phone_number, message, time_str):
    schedules.append({"phone": phone_number, "message": message, "time": time_str})

def send_reminders():
    while True:
        for event in schedules:
            # Check if the time matches (you can improve this logic)
            if event["time"] == time.strftime("%H:%M"):
                Tclient.messages.create(
                    body= event["message"],
                    from_=TWILIO_PHONE_NUMBER,
                    to= event["phone"]
                )
        time.sleep(60)  # Check every minute

@app.route("/process", methods=["POST", "GET"])
def process_request():
    data = request.json
    user_message = data["message"]
    user_phone = data["phone"]

    # AI model to interpret message
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

    try:
        parsed_data = eval(parsed_response)
        task = parsed_data["task"]
        date = parsed_data["date"]
        time = parsed_data["time"]

        # Save to schedules and send confirmation
        add_schedule(user_phone, f"Reminder: {task} at {time} on {date}", f"{time}")
        return jsonify({"status": "success", "message": "Reminder set!"})
    except Exception as e:
        return jsonify({"status": "error", "message": "Could not parse your request."})

# Start reminder thread
reminder_thread = Thread(target=send_reminders, daemon=True)
reminder_thread.start()

if __name__ == "__main__":
    app.run(debug=True)
