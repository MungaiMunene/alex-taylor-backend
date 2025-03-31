import schedule
import time
from datetime import datetime
from utils import send_message, generate_daily_summary

# Function to send daily message
def send_daily_message():
    # Get the message from OpenAI
    daily_message = generate_daily_summary()

    # Specify the phone number to send the message to
    user_phone_number = "+1234567890"  # Replace with the user's actual phone number

    # Send the message via Twilio
    result = send_message(user_phone_number, daily_message)
    print(result)

# Schedule the daily message at a specific time (e.g., 8 AM every day)
schedule.every().day.at("08:00").do(send_daily_message)

# Run the scheduler
if __name__ == "__main__":
    while True:
        schedule.run_pending()  # Run any scheduled tasks
        time.sleep(60)  # Wait for a minute before checking again