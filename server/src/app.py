from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from openai import OpenAI
import json
import time
from threading import Thread
import firebase_admin
from firebase_admin import firestore
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

# Initialize firestore
DB_app = firebase_admin.initialize_app()
db = firestore.client()

# Schedule for all reminders
schedules = []

# Parse for user intent
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

                                    Return only the number of the action
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

    return int(parsed_response)

def add_schedule(phone_number, task, time_str, date_str):
    schedules.append({"phone": phone_number, "task": task, "time": time_str, "date": date_str})

def delete_schedule(phone_number, task): # TODO: search through schedules for reminder to be deleted
    None 

# Functions for parsing user message
def parse_set(user_number, user_message):
    parsing_response = Oclient.chat.completions.create(
        model="gpt-4o-mini",
        messages= [
            {
                "role": "developer", 
                "content": [
                    {
                        "type": "text",
                        "text": "You parse user messages into separate structured JSON response with 'task', 'time', and 'date', if provided. Assume date is today if not provided. Translate time to 24 hour."
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

    # TODO: return whether task, date, time is missing
    if (task == None) | (date == None) | (time == None):
        return 0
    else:
        add_schedule(user_number, f"{task}", f"{time}", f"{date}")
        return 1

def parse_delete(user_number, user_message):
    parsing_response = Oclient.chat.completions.create(
        model="gpt-4o-mini",
        messages= [
            {
                "role": "developer", 
                "content": [
                    {
                        "type": "text",
                        "text": "You parse user messages into separate structured JSON response with 'task', 'time', and 'date', if provided. Assume date is today if not provided. Translate time to 24 hour."
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

    # TODO: return whether task, date, time is missing
    if (task == None):
        return 0
    else:
        delete_schedule(user_number, f"{task}")
        return 1

def parse_edit(user_number, user_message):
    parsing_response = Oclient.chat.completions.create(
        model="gpt-4o-mini",
        messages= [
            {
                "role": "developer", 
                "content": [
                    {
                        "type": "text",
                        "text": "You parse user messages into separate structured JSON response with 'original task', 'new time', and 'new date', if provided. Assume date is today if not provided. Translate time to 24 hour."
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
    task_original = parsed_data["original task"]
    date_new = parsed_data["new date"]
    time_new = parsed_data["new time"]

    # TODO: return whether task, date, time is missing
    if (task_original == None):
        return 0
    else:
        delete_schedule(user_number, f"{task_original}")
        add_schedule(user_number, f"{task_original}", f"{time_new}", f"{date_new}")
        return 1

def parse_list(user_number, user_message):
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

    parsed_data = json.loads(parsed_response)
    date = parsed_data["date"]
    time_frame = parsed_data["time frame"]

    # TODO: search through data base for timeframe/date
    return None

parse_array = [parse_set, parse_delete, parse_edit, parse_list]

    
# OpenAI assistant
Assistant = Oclient.beta.assistants.create(
    name="Marley", 
    instructions="""
                    You are a friendly personal assistant named Marley that help set reminders and centralize to-do lists. 
                    You are a texting assistant and able to set reminders. Do not say you cannot set reminders.
                    """,
    model="gpt-4o-mini", 
    temperature=1.0,
    top_p=1.0,
    tools=[]
)

# Endpoint for creating conversation once phone number is received
@app.route("/create_conversation", methods=["GET", "POST"])
def create_conversation():
    user_phone = request.form.get("phone")

    phone_ref = db.collection("Conversations").document(f"{user_phone}").get()

    if phone_ref.exists:
        #TODO: send a message to user
        None
        return jsonify({'This phone number already exists': f"{user_phone}"})

    else:

            # Create new twilio conversation
        conversation = Tclient.conversations.v1.conversations.create(
                friendly_name=f"Conversation with {user_phone}"
            )
        # conversations[user_phone] = conversation.sid 
            # Add conversation to firestore collection where document name is phone number 
        convo_ref = db.collection("Conversations").document(f"{user_phone}")
        convo_ref.set({"ID": f"{conversation.sid}"})

            # Add participant to new conversation
        participant = Tclient.conversations.v1.conversations(
                conversation.sid
            ).participants.create(
                messaging_binding_address=user_phone,
                messaging_binding_proxy_address=TWILIO_PHONE_NUMBER
            )

            # Create OpenAI thread
        thread = Oclient.beta.threads.create()
        # threads[user_phone] = thread.id # Add thread to dictionary
            # Add thread id to firestore collection where document name is phone number
        thread_ref = db.collection("Threads").document(f"{user_phone}")
        thread_ref.set({"ID": f"{thread.id}"})

            # Add message to thread
        message = Oclient.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content="Hello!"
            )

            # Run assistant on thread
        run = Oclient.beta.threads.runs.create_and_poll(
                thread_id=thread.id,
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

@app.route("/receive_message", methods=["POST"])
def sms_reply():
    # Get the message from the incoming request
    from_number = request.form.get("From")  # Sender's phone number
    user_message = request.form.get("Body")  # Message body
    #print(f"Received message from {from_number}: {user_message}") TODO: Change this to logging

    # Get thread id
    thread_ref = db.collection("Threads").document(f"{from_number}").get()
    if thread_ref.exists:
        Thread_id = thread_ref.to_dict()["ID"]
    
    # Get conversation sid
    convo_ref = db.collection("Conversations").document(f"{from_number}").get()
    if convo_ref.exists:
        Convo_id = convo_ref.to_dict()["ID"]
    
    # Add message to OpenAI threads
    message = Oclient.beta.threads.messages.create(
        thread_id=Thread_id,
        role="user",
        content=user_message
    )

    # Determine intent
    i = intent(user_message)

    if i != 4:
        # parse information based on intent
        p = parse_array[i](from_number, user_message)
        if p == 0:
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
            # Append to threads
            message = Oclient.beta.threads.messages.create(
                thread_id=Thread_id,
                role="assistant",
                content=message_final
            )
    # TODO: generate response ???
    else:
        # Run assistant on message thread
        run = Oclient.beta.threads.runs.create_and_poll(
            thread_id=Thread_id,
            assistant_id=Assistant.id
        )
        if run.status == 'completed': 
            messages = Oclient.beta.threads.messages.list(
                thread_id=Thread_id, order="desc", limit=3
            )
            message_final = messages.data[0].content[0].text.value # Get the latest message
        else:
            print(run.status)

    # Send response back using twilio conversation
    message = Tclient.conversations.v1.conversations(
        Convo_id
    ).messages.create(
        body=message_final
    )
    return jsonify({"Return message": message_final})

@app.route("/reminder_thread", methods=["POST"])
def reminder_thread():
    for event in schedules:
        # TODO: improve time logic
        if event["time"] == time.strftime("%H:%M"):
            task = event["task"]
            number = event["phone"]
            
            # Create message through OpenAI api
            message = Oclient.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "developer", 
                        "content": [
                            {
                                "type": "text",
                                "text": "You create reminders based off of the specified user task" 
                            }
                        ]
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"{task}"
                            }
                        ]
                    }
                ]
            )
            message_final = message.choices[0].message.content

            # Append to threads
                # Get thread id
            thread_ref = db.collection("Threads").document(f"{number}").get()
            if thread_ref.exists:
                Thread_id = thread_ref.to_dict()["ID"]
                message = Oclient.beta.threads.messages.create(
                    thread_id=Thread_id,
                    role="assistant",
                    content=message_final
                )


            # Send through twilio conversation
                 # Get conversation sid
            convo_ref = db.collection("Conversations").document(f"{number}").get()
            if convo_ref.exists:
                Convo_id = convo_ref.to_dict()["ID"]
                message = Tclient.conversations.v1.conversations(
                    Convo_id
                ).messages.create(
                    body=message_final
                )

            #print(f"Task: {event['task']}, Phone: {event['phone']}, Time: {event['time']}, Date: {event['date']}")
    return jsonify({"Return message": "Place holder return message"})

@app.route("/testing", methods=["GET"])
def testing():
    number = "+12063343224"
    ID = "RANDOM010101ID"

    doc_ref = db.collection("Testing").document(f"{number}")
    doc_ref.set({"ID": f"{ID}", "Message": "This is the ship that made the Kessel Run in fourteen parsecs?"})

    users_ref = db.collection("Testing").document(f"{number}")
    doc = users_ref.get()

    if doc.exists:
        dicti = doc.to_dict()
        m = dicti["Message"]
        
        message = Tclient.messages.create(
            body=m,
            from_=TWILIO_PHONE_NUMBER,
            to=number
        )
    else:
        print("No such document!")
    

    return "<p>This is the ship that made the Kessel Run in fourteen parsecs?</p>"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
