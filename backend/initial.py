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

# TODO: create/link twilio conversations database where phone number and conversation.sid are stored as key-value pairs
# TODO: create/link openai threads database where phone number and thread.id are stored as key-value pairs 
# TODO: get assistant.id

@app.route("/create_conversation", methods=["POST"])
def create_conversation():
    user_phone = request.form.get("phoneNumber")
    # TODO: ensure phone numbers are all in same format

    # TODO: ensure phone number is not already in database

    # Create new twilio conversation
    conversation = Tclient.conversations.v1.conversations.create(
            friendly_name=f"Conversation with {user_phone}"
        )
    
    # TODO:
    conversations[user_phone] = conversation.sid # Add conversation to dictionary

    # Add participant to new conversation
    participant = Tclient.conversations.v1.conversations(
            conversation.sid
        ).participants.create(
            messaging_binding_address=user_phone,
            messaging_binding_proxy_address=TWILIO_PHONE_NUMBER
        )

    # Create OpenAI thread
    thread = Oclient.beta.threads.create()
    # TODO:
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

    return jsonify({
        'conversation_sid': conversation.sid,
        'participant_sid': participant.sid,
        'phone_number': user_phone
    })


if __name__ == "__main__":
    app.run(debug=True)