from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__)

@app.route("/sms", methods=["POST", "GET"])
def sms_reply():
    """Respond to incoming SMS with a custom message."""
    # Get the message from the incoming request
    from_number = request.form.get("From")  # Sender's phone number
    body = request.form.get("Body")        # Message body
    
    print(f"Received message from {from_number}: {body}")

    # Create a response message to send back to the user
    response = MessagingResponse()

    # Customize the reply message
    response.message("Thank you for your message! We will get back to you shortly.")
    
    return str(response)

if __name__ == "__main__":
    app.run(debug=True)