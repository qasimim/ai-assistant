# process_speech.py
from fastapi import APIRouter, Response, Form
from twilio.twiml.voice_response import VoiceResponse
from ..utils.rasa_utils import send_to_rasa
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/process-speech")
async def process_speech(SpeechResult: str = Form(...), Caller: str = Form(...)):
    logger.info(f"Processing speech input from caller: {Caller}")
    try:
        rasa_response = send_to_rasa(Caller, SpeechResult)
        response = VoiceResponse()
        response.say(rasa_response)
        response.gather(input='speech', action='/process-speech', method='POST')
        return Response(content=str(response), media_type="application/xml")
    except Exception as e:
        logger.error(f"Error processing speech input from caller {Caller}: {e}", exc_info=True)
        raise e
