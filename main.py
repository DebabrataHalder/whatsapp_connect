import os
from fastapi import FastAPI, Form, Depends
from dotenv import load_dotenv
from groq import Groq
from twilio.twiml.messaging_response import MessagingResponse
from fastapi.responses import PlainTextResponse

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Initialize the Groq client using the API key from the .env file
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.post("/whatsapp", response_class=PlainTextResponse)
def whatsapp(body: str = Form(...)):
    # Use the Groq API to generate a chat completion based on the incoming message
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": body},
        ],
        model="llama-3.3-70b-versatile",
    )
    reply = chat_completion.choices[0].message.content
    
    # Create a Twilio MessagingResponse to send the reply back to WhatsApp
    response = MessagingResponse()
    response.message(reply)
    
    return str(response)

