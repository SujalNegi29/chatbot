import requests

RASA_URL = "http://localhost:5005/webhooks/rest/webhook"

def send_to_rasa(message, sender="user"):
    payload = {
        "sender": sender,
        "message": message
    }
    response = requests.post(RASA_URL, json=payload)
    return response.json()
