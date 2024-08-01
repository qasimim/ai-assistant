# voice.py
from fastapi import APIRouter, Response, Request, HTTPException
from twilio.twiml.voice_response import VoiceResponse, Gather
from datetime import datetime
from ..database import database
from ..models import user_interactions, issues
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/voice")
async def handle_voice(request: Request):
    form_data = await request.form()
    caller_number = form_data.get("Caller")
    call_sid = form_data.get("CallSid")

    query = user_interactions.insert().values(
        user_id=caller_number,
        call_sid=call_sid,
        message="Call initiated",
        response="",
        timestamp=datetime.now(),
        call_duration=None
    )
    await database.execute(query)
    logger.info(f"Call session started with SID {call_sid} for caller {caller_number}")

    response = VoiceResponse()
    response.say("Welcome to our service. Please say something after the beep.")

    gather = Gather(input='speech', action='/process-speech', method='POST')
    response.append(gather)

    response.redirect('/status-callback', method='POST')

    return Response(content=str(response), media_type="application/xml")

@router.post("/status-callback")
async def status_callback(request: Request):
    form_data = await request.form()
    call_status = form_data.get("CallStatus")
    call_sid = form_data.get("CallSid")
    call_duration_str = form_data.get("CallDuration")

    try:
        if call_duration_str is not None:
            call_duration = int(call_duration_str)
        else:
            logger.warning(f"CallDuration not provided for call SID {call_sid}. Setting call duration to 0.")
            call_duration = 0

        if call_status == "completed" and call_duration > 0:
            update_query = user_interactions.update().\
                where(user_interactions.c.call_sid == call_sid).\
                values(call_duration=call_duration)
            await database.execute(update_query)
            logger.info(f"Call with SID {call_sid} updated with duration {call_duration}")
    except Exception as e:
        logger.error(f"Error updating call duration for call SID {call_sid}: {e}", exc_info=True)

    return {"status": "success"}

class CustomerData(BaseModel):
    phone_number: str
    customer_name: str
    customer_zipcode: str

@router.post("/customer")
async def handle_customer_data(customer_data: CustomerData):
    try:
        await check_and_update_or_create_customer(
            customer_data.phone_number,
            customer_data.customer_name,
            customer_data.customer_zipcode
        )
        logger.info(f"Customer data processed for {customer_data.phone_number}")
        return {"message": "Customer data processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
class IssueData(BaseModel):
    phone_number: str
    issue_description: str
    issue_expected_date: str

@router.post("/create-issue")
async def create_issue(issue_data: IssueData):
    query = issues.insert().values(
        phone_number=issue_data.phone_number,
        issue_description=issue_data.issue_description,
        issue_start_date=datetime.now(),
        issue_expected_date=issue_data.issue_expected_date,
        status="open"
    )
    await database.execute(query)
    logger.info(f"Issue created for {issue_data.phone_number} with description: {issue_data.issue_description}")
    return {"message": "Issue created successfully"}
