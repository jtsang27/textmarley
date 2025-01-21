from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from openai import OpenAI
import json
import time
from threading import Thread
import os

app = Flask(__name__)

# Twilio credentials
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# OpenAI api key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Clients
Tclient = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
Oclient = OpenAI(api_key=OPENAI_API_KEY)

def send_message(message, number):
    Tclient.messages.create(
        body= message, 
        from_=TWILIO_PHONE_NUMBER,
        to= f"{number}" 
    )

def add_schedule(phone_number, task, time_str, date_str):
    schedules.append({"phone": phone_number, "task": task, "time": time_str, "date": date_str})

def parse_reminder(user_message, user_number):
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

    parsed_data = json.loads(parsed_response)
    task = parsed_data["task"]
    date = parsed_data["date"]
    time = parsed_data["time"]

    if (task == None) | (date == None) | (time == None):
        return 0
    else:
        add_schedule(user_number, f"{task}", f"{time}", f"{date}")
    
def send_reminders():
    while True:
        for event in schedules:
            # Check if the time matches (you can improve this logic)
            if event["time"] == time.strftime("%H:%M"):
                # Create message through OpenAI api
                task = event["task"]
                number = event["phone"]
                send_message(task, number)
            print(event['phone'])
            print(event['task'])
            print(event['time'])
            print(event['date'])
        time.sleep(60)  # Check every minute

# Schedule for all reminders
schedules = []
# Store twilio conversations
conversations = {}
# Store openai threads
threads = {}

# OpenAI assistant
Assistant = Oclient.beta.assistants.create(
    name="Marley", 
    instructions="You are a friendly personal assistant that help set reminders and centralize to-do lists.",
    model="gpt-4o-mini", 
    temperature=1.0,
    top_p=1.0,
    tools=[]
)

# Endpoint for creating conversation once phone number is received
@app.route("/create_conversation", methods=["POST"])
def create_conversation():
    user_phone = request.form.get("phoneNumber")
    # TODO: ensure phone numbers are all in same format

    
        # Create new twilio conversation
    conversation = Tclient.conversations.v1.conversations.create(
            friendly_name=f"Conversation with {user_phone}"
        )
    conversations[user_phone] = conversation.sid # Add conversation to dictionary
    print(conversations)

        # Add participant to new conversation
    participant = Tclient.conversations.v1.conversations(
            conversation.sid
        ).participants.create(
            messaging_binding_address=user_phone,
            messaging_binding_proxy_address=TWILIO_PHONE_NUMBER
        )

        # Create OpenAI thread
    thread = Oclient.beta.threads.create()
    threads[user_phone] = thread.id # Add thread to dictionary

        # Add message to thread
    message = Oclient.beta.threads.messages.create(
            thread_id=threads[user_phone],
            role="user",
            content="Hello!"
        )

        # Run assistant on thread
    run = Oclient.beta.threads.runs.create_and_poll(
            thread_id=threads[user_phone],
            assistant_id=Assistant.id,
        )

    if run.status == 'completed': 
            messages = Oclient.beta.threads.messages.list(
                thread_id=thread.id, order="desc", limit=3
            )
            send = messages.data[0].content[0].text.value # Get the latest message
    else:
            print(run.status)

        # Send initial message
    message = Tclient.conversations.v1.conversations(
            conversation.sid
        ).messages.create(
            body=send
        )

    #except:
    #    return jsonify({'Error': "Conversation with this number already exists"})

    return jsonify({
        'conversation_sid': conversation.sid,
        'participant_sid': participant.sid,
        'phone_number': user_phone
    })

@app.route("/receive_message", methods=["POST"])
def sms_reply():
    """Respond to incoming SMS with a custom message."""
    # Get the message from the incoming request
    from_number = request.form.get("From")  # Sender's phone number
    user_message = request.form.get("Body")        # Message body
    print(f"Received message from {from_number}: {user_message}")
    print(threads)
    # Add message to OpenAI threads
    message = Oclient.beta.threads.messages.create(
        thread_id=threads[from_number],
        role="user",
        content=user_message
    )

    # Stores reminder information 
    i = parse_reminder(user_message, from_number)

    if i == 0:
        message_final = "Please be more specific in you reminder request"
    else: 
        print(f"Reminder stored: {schedules}")
        # Create a response message to send back to the user
        message = Oclient.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "developer", 
                    "content": [
                        {
                            "type": "text",
                            "text": "You create automatic responses to confirm users' reminder requests"
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
            ]
        )
        message_final = message.choices[0].message.content

    # Send response back using twilio conversation
    message = Tclient.conversations.v1.conversations(
        conversations[from_number]
    ).messages.create(
        body=message_final
    )
    return jsonify({"Return message": message_final})

# Start reminder thread
reminder_thread = Thread(target=send_reminders, daemon=True)
reminder_thread.start()

if __name__ == "__main__":
    app.run(debug=True)
