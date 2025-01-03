from flask import Flask, request, jsonify
from twilio.rest import Client
import openai
import schedule
import time
from threading import Thread

app = Flask(__name__)

# Twilio credentials
TWILIO_SID = "ACd1fc272aaed14e7c30cec526df3fab44"
TWILIO_AUTH_TOKEN = "11258e6372a073bbfb018de8d1737938"
TWILIO_PHONE_NUMBER = "+18444406910"

# OpenAI API key
OPENAI_API_KEY = "your_openai_api_key"

# Initialize Twilio client
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# Database to store user schedules
schedules = []

def add_schedule(phone_number, message, time_str):
    schedules.append({"phone": phone_number, "message": message, "time": time_str})

def send_reminders():
    while True:
        for event in schedules:
            # Check if the time matches (you can improve this logic)
            if event["time"] == time.strftime("%H:%M"):
                client.messages.create(
                    body=event["message"],
                    from_=TWILIO_PHONE_NUMBER,
                    to=event["phone"]
                )
        time.sleep(60)  # Check every minute

@app.route("/process", methods=["POST"])
def process_request():
    data = request.json
    user_message = data["message"]
    user_phone = data["phone"]

    # AI model to interpret message
    openai.api_key = OPENAI_API_KEY
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Parse this schedule request: '{user_message}'. Provide a structured JSON response with 'task', 'time', and 'date'.",
        max_tokens=100
    )
    parsed_response = response.choices[0].text.strip()

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
