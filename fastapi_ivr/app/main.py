# app/main.py
from fastapi import FastAPI, Request
from .routes import process_speech, voice, chat
from .database import database, metadata, engine
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import logging.config
from .utils.logging_config import LOGGING_CONFIG

metadata.create_all(engine)
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)
app = FastAPI()

main_app_lifespan = app.router.lifespan_context

@asynccontextmanager
async def lifespan_wrapper(app: FastAPI):
    async with main_app_lifespan(app) as maybe_state:
        logger.info("Custom startup logic")
        await database.connect()

        yield maybe_state

        logger.info("Custom shutdown logic")
        await database.disconnect()

app.router.lifespan_context = lifespan_wrapper

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def ngrok_skip_browser_warning(request: Request, call_next):
    response = await call_next(request)
    response.headers['ngrok-skip-browser-warning'] = 'true'
    return response

app.include_router(voice.router)
app.include_router(process_speech.router)
app.include_router(chat.router)
