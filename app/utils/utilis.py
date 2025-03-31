import os
from twilio.rest import Client
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twilio Configuration
TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')  # The Twilio number for WhatsApp/SMS

# OpenAI API Key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Twilio Client
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# Function to send SMS or WhatsApp message using Twilio
def send_message(to, message):
    try:
        msg = client.messages.create(
            to=to,
            from_=TWILIO_PHONE_NUMBER,  # Your Twilio number
            body=message
        )
        return f"Message sent: {msg.sid}"
    except Exception as e:
        return f"Failed to send message: {str(e)}"

# OpenAI Function to generate daily summary and motivational messages
def generate_daily_summary():
    prompt = """
    Generate a motivational message for the day that includes:
    - A good morning greeting.
    - A quick recap of the day's schedule.
    - A reminder of the key productivity goals.
    - A motivational statement to encourage the user.
    """
    
    response = openai.Completion.create(
        engine="text-davinci-003",  # Use the appropriate GPT model
        prompt=prompt,
        max_tokens=150,  # Adjust token count as needed
        temperature=0.7  # Adjust creativity level
    )

    return response.choices[0].text.strip()