#rasa_utils.py
import logging
import requests
import os

RASA_SERVER_URL = os.getenv('RASA_SERVER_URL', 'http://localhost:5005/webhooks/rest/webhook')
logger = logging.getLogger(__name__)

def send_to_rasa(caller_number, user_input):
    data = {"sender": caller_number, "message": user_input}
    try:
        response = requests.post(RASA_SERVER_URL, json=data)
        if response.status_code == 200:
            rasa_data = response.json()
            return rasa_data[0]['text']
        else:
            logger.error(f"Non-200 status code received from Rasa server: {response.status_code}")
            return "I'm having trouble understanding. Please try again."
    except Exception as e:
        logger.error(f"Exception occurred while sending data to Rasa: {e}", exc_info=True)
        return "I'm having trouble understanding. Please try again."
