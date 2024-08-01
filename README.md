
# FastAPI IVR Application

## Overview
This project is a powerful Interactive Voice Response (IVR) system designed for the plumbing industry. It enables users to interact via voice calls, providing a seamless experience for scheduling appointments, obtaining service information, and managing inquiries. The system leverages advanced voice recognition and natural language processing to understand and respond to user commands dynamically. It streamlines communication, making it easier for customers to access services and for service providers to manage customer interactions efficiently.


## Features
- Voice Interaction: Uses Twilio for voice recognition and response.
- Natural Language Understanding: Integrates Rasa for understanding and responding to user queries.
- Database Integration: Stores user interactions and issues in a PostgreSQL database.
- Containerization: Dockerized for easy deployment using Docker Compose.

## Technologies Used
- FastAPI: A modern, fast (high-performance) web framework for building APIs with Python 3.7+.
- Rasa: An open-source machine learning framework for building contextual AI assistants.
- Twilio: A cloud communications platform for making and receiving voice calls.
- PostgreSQL: An advanced open-source relational database.
- Docker: A set of platform-as-a-service products that use OS-level virtualization to deliver software in packages called containers.


## Installation

### Prerequisites
- Docker
- Docker Compose
- Twilio Account (for voice functionality)
- ngrok

### Setup

1. Clone the Repository:
   ```
   git clone https://github.com/qasimim/ai-assistant.git
   cd ivr-app
   ```

2. Build and Start Services:
   ```
   docker-compose up --build
   ```

3. Access the Services:
   - FastAPI Application: http://localhost:8000
   - Rasa Core/NLU: http://localhost:5005
   - Rasa Actions Server: http://localhost:5055

### Important Environment Variables

- Security Sensitive:
  - DATABASE_URL: URL for the PostgreSQL database.
  - RASA_SERVER_URL: URL for the Rasa server.
  - TWILIO_ACCOUNT_SID: Your Twilio account SID.
  - TWILIO_AUTH_TOKEN: Your Twilio Auth Token.
  - TWILIO_PHONE_NUMBER: Your Twilio phone number for making/receiving calls.

Ensure these environment variables are set appropriately in the Docker Compose file or passed during container startup to avoid exposing sensitive information.

### Example Conversation Flow

User: "Hello, I need help with my plumbing."
Bot: "Hello! I'm here to assist you. Could you please describe the problem you're experiencing?"
User: "My sink has been leaking water slowly, and it's been getting worse over the past few days."
Bot: "I'm sorry to hear that. Have you noticed if the leak is continuous or if it happens at specific times?"
User: "It seems to be continuous, even when the faucet is off."
Bot: "Thank you for the details. Could you please provide your name so we can log your request?"
User: "My name is Jane Doe."
Bot: "Thanks, Jane. For our records, could you also provide your phone number?"
User: "Sure, it's 555-1234."
Bot: "Great, and could you tell me your address so we can send a technician?"
User: "I live at 456 Elm Street, Springfield."
Bot: "Got it, 456 Elm Street, Springfield. Is this a house or an apartment?"
User: "It's a house."
Bot: "Understood. Could you let us know when would be a convenient time for a technician to visit?"
User: "I would prefer tomorrow morning, if possible."
Bot: "We can schedule a technician between 9 AM and 12 PM tomorrow. Does that work for you?"
User: "Yes, that works."
Bot: "Perfect. Just to confirm, a technician will visit 456 Elm Street, Springfield tomorrow between 9 AM and 12 PM. Is there anything else you need help with?"
User: "Yes, I'm also concerned about my water heater; it hasn't been working properly."
Bot: "Can you tell me more about the issue with the water heater? Is it not heating water at all, or is the issue intermittent?"
User: "It's intermittent. Sometimes it works, but often the water only gets lukewarm."
Bot: "Thank you for the additional information. We'll make sure the technician is aware of both issues. Is there anything else you'd like to add?"
User: "No, that's all for now."
Bot: "Great. We'll see you tomorrow morning. If you need to reschedule or have any other questions, please don't hesitate to contact us. Thank you, Jane, and have a great day!"
User: "Thank you, goodbye."
Bot: "Goodbye, and take care!"




### Visual Diagram:

```
User Call
  ↓
Twilio (Webhook to FastAPI /voice)
  ↓
FastAPI /voice Endpoint
  │→ Extract Caller Info
  │→ Log in PostgreSQL ('user_interactions')
  │→ Generate TwiML Response
  ↓
Twilio (Speech Processing)
  ↓
FastAPI /process-speech Endpoint
  │→ Forward Transcript to Rasa
  │→ Rasa Processes Intent and Responds
  │→ Log Interaction in PostgreSQL ('user_interactions')
  │→ Prepare TwiML Response
  ↓
Twilio (Deliver Rasa's Response to User)
  ↓
Call Ends (Twilio sends to /status-callback)
  ↓
FastAPI /status-callback Endpoint
  │→ Log Call Duration in PostgreSQL ('user_interactions')
  │→ Update Call Session
  ↓
Optional PostgreSQL Updates
  │→ CRUD Operations on 'customers' and 'issues' Tables
```

## Contributing
Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

---
