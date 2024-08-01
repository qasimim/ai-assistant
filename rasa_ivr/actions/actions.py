#actions.py
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, SlotSet
import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class ActionRepeatLastPhrase(Action):
    def name(self) -> Text:
        return "action_repeat_last_phrase"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        for event in reversed(tracker.events):
            if event["event"] == "bot":
                dispatcher.utter_message(text=event["text"])
                break
        return [UserUtteranceReverted()]


class ActionUserZipcodeGiven(Action):
    def name(self) -> Text:
        return "action_user_zipcode_given"
    
    async def run(
            self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    
        user_zipcode = tracker.get_slot("user_zipcode")
        return [SlotSet("user_zipcode_given", bool(user_zipcode))]


class ActionConfirmIssueDate(Action):
    def name(self) -> Text:
        return "action_confirm_issue_date"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict[Text, Any]]:
        issue_day = tracker.get_slot("issue_day")
        issue_time = tracker.get_slot("issue_time")
        
        if issue_day and issue_time:
            dispatcher.utter_message(text=f"Do you want to set the appointment for {issue_day} at {issue_time}?")
        elif not issue_day:
            dispatcher.utter_message(text="Could you please tell me what day you'd like to schedule the appointment?")
        elif not issue_time:
            dispatcher.utter_message(text=f"What time on {issue_day}?")
        
        return []


class ActionResetIssueDate(Action):
    def name(self) -> Text:
        return "action_reset_issue_date"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict[Text, Any]]:
        return [SlotSet("issue_day", None), SlotSet("issue_time", None)]


class ActionUserNameGiven(Action):
    def name(self) -> Text:
        return "action_user_name_given"
    
    async def run(
            self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    
        user_name = tracker.get_slot("PERSON")
        return [SlotSet("user_name_given", bool(user_name))]


class ActionConfirmEverything(Action):
    def name(self) -> Text:
        return "action_confirm_everything"
    
    async def run(
            self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    
        issue_day = tracker.get_slot("issue_day")
        issue_time = tracker.get_slot("issue_time")
        user_address = tracker.get_slot("user_address")
        user_name = tracker.get_slot("PERSON")

        if not issue_day:
            dispatcher.utter_message(response="utter_ask_availability")
        elif not user_address:
            dispatcher.utter_message(text="I'm sorry, I didn't get your address. Could you tell me your address?")
        else:
            dispatcher.utter_message(text=f"Thank you {user_name} for the information. Our technician will be at {user_address} by {issue_day} at {issue_time}. Please let me know if you have any more questions.")
        return []


class ActionChatGPTResponse(Action):
    def name(self) -> Text:
        return "action_chatgpt_response"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.latest_message['intent'].get('name') == "intent_describe_issue_in_detail":
            user_message = tracker.latest_message.get('text')
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {os.getenv("OPENAI_API_KEY")}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': "gpt-3.5-turbo",
                    'messages': [
                        {'role': 'system', 'content': 'You are integrated into a Rasa chatbot as a plumbing assistant. Provide empathetic responses without offering solutions or asking further questions.'},
                        {'role': 'user', 'content': user_message}
                    ],
                    'max_tokens': 100
                }
            )

            if response.status_code == 200:
                chatgpt_response = response.json()
                gpt_message = chatgpt_response["choices"][0]["message"]["content"]
                dispatcher.utter_message(text=gpt_message)
            else:
                dispatcher.utter_message(text="Sorry, I couldn't generate a response at the moment. Please try again later.")
                return [UserUtteranceReverted()]

        return []


class ActionChatGPTResponseOutOfScope(Action):
    def name(self) -> Text:
        return "action_chatgpt_response_out_of_scope"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.latest_message['intent'].get('name') == "intent_out_of_scope":
            user_message = tracker.latest_message.get('text')
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {os.getenv("OPENAI_API_KEY")}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': "gpt-3.5-turbo",
                    'messages': [
                        {'role': 'system', 'content': 'You are integrated into a Rasa chatbot as a plumbing assistant. Provide empathetic responses without offering solutions or asking further questions.'},
                        {'role': 'user', 'content': user_message}
                    ],
                    'max_tokens': 100
                }
            )

            if response.status_code == 200:
                chatgpt_response = response.json()
                gpt_message = chatgpt_response["choices"][0]["message"]["content"]
                dispatcher.utter_message(text=gpt_message)
            else:
                dispatcher.utter_message(text="Sorry, I couldn't generate a response at the moment. Please try again later.")
                return [UserUtteranceReverted()]

        return []


class ActionSaveCustomerInfo(Action):
    def name(self) -> str:
        return "action_save_customer_info"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        person_name = tracker.get_slot('PERSON')
        zipcode = tracker.get_slot('user_zipcode')
        user_address = tracker.get_slot('user_address')
        user_id = tracker.sender_id

        payload = {
            "phone_number": user_id,
            "customer_name": person_name,
            "customer_address": user_address,
            "customer_zipcode": zipcode
        }

        logging.info(f"Sending customer data to FastAPI: {payload}")
        response = requests.post("http://localhost:8000/customer", json=payload)
        logging.info(f"Received response: Status code: {response.status_code}, Body: {response.text}")

        if response.status_code == 200:
            dispatcher.utter_message(text="Your information has been saved.")
        else:
            logging.error(f"Failed to save customer information. Status code: {response.status_code}, Response: {response.text}")
            dispatcher.utter_message(text="Failed to save customer information.")
        
        return []


class ActionReportIssue(Action):
    def name(self) -> Text:
        return "action_report_issue"

    async def run(self, dispatcher, tracker, domain):
        issue_description = tracker.get_slot('issue_description_detailed')
        issue_expected_date = tracker.get_slot('issue_day')
        phone_number = tracker.sender_id

        response = requests.post(
            "http://localhost:8000/create-issue",
            json={
                "phone_number": phone_number,
                "issue_description": issue_description,
                "issue_expected_date": issue_expected_date
            }
        )
        if response.status_code == 200:
            dispatcher.utter_message("Issue reported successfully.")
        else:
            dispatcher.utter_message("Failed to report the issue.")

        return []
