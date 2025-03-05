from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from openai import OpenAI
import json
from datetime import datetime
import pytz
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

def standardize_time(date_str, time_str, user_timezone="America/New_York"):
    if not date_str: # Check if date is provided, if now, assume today
        date_str = datetime.now(pytz.utc).strftime("%Y-%m-%d")

    # Convert parsed strings to a datetime object
    naive_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")

    # Set the correct timezone
    user_tz = pytz.timezone(user_timezone)
    localized_dt = user_tz.localize(naive_dt)

    # Convert to UTC
    utc_dt = localized_dt.astimezone(pytz.utc).isoformat()

    return utc_dt  # Return datetime in UTC

def add_reminder(user_number, task, date, time, recurring=False, frequency=None):
    reminder_ref = db.collection("Reminders").document()
    reminder_ref.set({
        "user_number": user_number,
        "task": task,
        "time": standardize_time(date, time), 
        "recurring": recurring,
        "frequency": frequency,
        "status": "Pending"
    })

def delete_reminder(user_number, task, date, time):
    time_ = standardize_time(date, time)
    to_delete = db.collection("Reminders").where("user_number", "==", user_number).where("task", "==", task).where("time", "==", time_)
    db.collection("Reminders").document(to_delete.id).delete()

def get_reminders(user_number):
    now = datetime.now(pytz.UTC).replace(second=0, microsecond=0).isoformat()
    reminders = db.collection("Reminders").where("user_number", "==", user_number).where("time", ">=", now).where("status", "==", "Pending").order_by("time").stream()

    schedule = []
    for reminder in reminders:
        d = reminder.to_dict()
        task = d.get("task")
        time = d.get("time")

        # Convert to datetime object
        dt_obj = datetime.fromisoformat(time)
        if dt_obj.tzinfo is None:
            # Add timezone
            dt_obj = dt_obj.replace(tzinfo=pytz.timezone('US/Eastern'))

        # Convert to UTC
        est_dt = dt_obj.astimezone(pytz.timezone('US/Eastern')).isoformat()

        schedule.append((task, est_dt))
    return schedule

# Functions for parsing user message
def parse_set(user_number, user_message): # TODO: add parsing for frequency
    parsing_response = Oclient.chat.completions.create(
        model="gpt-4o-mini",
        messages= [
            {
                "role": "developer", 
                "content": [
                    {
                        "type": "text",
                        "text": f"""You parse user messages into separate structured JSON response with 'task', 'date', 'time', 
                                'recurring', and 'frequency' if provided. Time must be in 24-hour format (HH:MM) and date in YYYY-MM-DD. 
                                Today's date and time is {datetime.now(pytz.timezone("America/New_York")).strftime("%Y-%m-%d %H:%M")}, 
                                if not provided by user or if user specifys today. If user asks for tomorrow or in the future, use this date to calculate.
                                Convert phrases like 'in 5 minutes' or 'in an hour' into an absolute time based off today's time. 
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

    parsed_data = json.loads(parsed_response)
    task = parsed_data.get("task")
    date = parsed_data.get("date") 
    time = parsed_data.get("time")
    recurring = parsed_data.get("recurring", False)
    frequency = parsed_data.get("frequency", None)

    if task and time:
        add_reminder(user_number, task, date, time, recurring, frequency)
    return {"task": task, "time": time}

def parse_delete(user_number, user_message):
    parsing_response = Oclient.chat.completions.create(
        model="gpt-4o-mini",
        messages= [
            {
                "role": "developer", 
                "content": [
                    {
                        "type": "text",
                        "text": """You parse user messages into separate structured JSON response with 'task', 'date' and 'time', if provided. 
                        Time must be in 24-hour format (HH:MM) and date in YYYY-MM-DD. Assume today if no date is given."""
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
    task = parsed_data.get("task")
    date = parsed_data.get("date") # TODO: if no date entered, then this set as today
    time = parsed_data.get("time")

    # TODO: return whether task, date, time is missing
    if task and time:
        delete_reminder(user_number, task, date, time)
    return {"task": task, "time": time}

def parse_edit(user_number, user_message):
    parsing_response = Oclient.chat.completions.create(
        model="gpt-4o-mini",
        messages= [
            {
                "role": "developer", 
                "content": [
                    {
                        "type": "text",
                        "text": """You parse user messages into separate structured JSON response with 'original task', 'new date', and 'new time', if provided. 
                        Time must be in 24-hour format (HH:MM) and date in YYYY-MM-DD. Assume today if no date is given."""
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
    task_original = parsed_data.get("original task")
    date_new = parsed_data.get("new date")
    time_new = parsed_data.get("new time")

    if task_original and date_new and time_new:
        delete_reminder(user_number, task_original)
        add_reminder(user_number, task_original, date_new, time_new)
    return {"Original task": task_original, "New Date": date_new, "New time": time_new}

def parse_list(user_number, user_message):
    # parsing_response = Oclient.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages= [
    #         {
    #             "role": "developer", 
    #             "content": [
    #                 {
    #                     "type": "text",
    #                     "text": """You parse user messages into separate structured JSON response with 'time frame' and 'date', if provided. 
    #                                 If not provided, assume 'date' is today and 'time frame' is null"""
    #                 }
    #             ]
    #         },
    #         {
    #             "role": "user",
    #             "content": [
    #                 {
    #                     "type": "text",
    #                     "text": f"{user_message}"
    #                 }
    #             ]
    #         }
    #     ],
    #     max_tokens=100
    # )
    # parsed_response = parsing_response.choices[0].message.content

    # parsed_data = json.loads(parsed_response)
    # date = parsed_data["date"]
    # time_frame = parsed_data["time frame"]

    reminders = get_reminders(user_number)
    return reminders

parse_array = [parse_set, parse_delete, parse_edit, parse_list]

    
# OpenAI assistant
Assistant = Oclient.beta.assistants.create(
    name="Marley", 
    instructions=f"""
                    Pretend you are able to actually send SMS texts through a phone and never say you are not able to send 
                    actual texts to user phone number. You are a friendly personal assistant named Marley that helps college students 
                    manage their day-to-day deadlines, class homework, projects, meetings, etc. You proactively help students stay 
                    on top of commitments, and you communicate purely through texting/sms. You are fully able to set reminders and text users. 

                    You were created by Boston University Men's Swim and Dive team members Jonny Farber, Jonathan "Big Fish" Tsang, and Evan Liu, if any user inquires. 

                    Today's date and time is {datetime.now(pytz.timezone("America/New_York")).strftime("%Y-%m-%d %H:%M")}, if needed.
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
def receive_message():
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

    if i == 3: # Listing reminder case
        # Find all future reminders
        p = get_reminders(from_number)

        # Create a response message to send back to the user
        message = Oclient.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "developer", 
                    "content": [
                        {
                            "type": "text",
                            "text": """You convert the following list of schedules into a friendly schedule for the user."""
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"{p}"
                        }
                    ]
                }
            ], temperature=0.75
        )
        message_final = message.choices[0].message.content
        # Append to threads
        message = Oclient.beta.threads.messages.create(
            thread_id=Thread_id,
            role="assistant",
            content=message_final
        )

    elif i != 4 and i != 3: # Set, delete, or edit cases
        # Parse information based on intent
        p = parse_array[i](from_number, user_message)
         
        # Create a response message to send back to the user
        message = Oclient.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "developer", 
                    "content": [
                        {
                            "type": "text",
                            "text": """You create friendly automatic responses to confirm users' reminder requests, 
                            or ask for more information depending on the provided missing variables, if any."""
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"{user_message}, {p}"
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
    now = datetime.now(pytz.UTC).replace(second=0, microsecond=0).isoformat()
    reminders = db.collection("Reminders").where("time", "==", now).stream()
    for event in reminders:
        # Convert to dictionary and get reminder task and user number
        event = event.to_dict()
        task = event.get("task")
        number = event.get("user_number")

        # Create message through OpenAI api
        message = Oclient.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "developer", 
                    "content": [
                        {
                            "type": "text",
                            "text": "You create friendly reminders for a college student based off of the task they enter. Keep it brief. Do not say tell the user to set a reminder. Simply, remind them." 
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

    return jsonify({"Return message": "Place holder return message"})

@app.route("/delete_expired_reminders", methods=["POST"])
def delete_past_reminder(): 
    """
        Deletes past reminders that are over one day old. Only delete reminders that are not recurring
    """
    now = datetime.now(pytz.UTC).replace(hour=00, minute=00, second=0, microsecond=0).isoformat()
    reminders = db.collection("Reminders").where("time", "<", now).where("recurring", "==", False).stream()

    for reminder in reminders:
        db.collection("Reminders").document(reminder.id).delete()

    return jsonify({"Message": "Past reminders deleted"})

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
