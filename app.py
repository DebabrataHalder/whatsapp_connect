
import os
from flask import Flask, request
from dotenv import load_dotenv
from groq import Groq
from twilio.twiml.messaging_response import MessagingResponse

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Initialize the Groq client using the API key from the .env file
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    # Extract the incoming WhatsApp message from the request body
    incoming_msg = request.values.get("Body", "")
    
    # Use the Groq API to generate a chat completion based on the incoming message
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": incoming_msg},
        ],
        model="llama-3.3-70b-versatile",
    )
    reply = chat_completion.choices[0].message.content
    
    # Create a Twilio MessagingResponse to send the reply back to WhatsApp
    response = MessagingResponse()
    response.message(reply)
    
    return str(response)

if __name__ == "__main__":
    app.run(debug=True)
