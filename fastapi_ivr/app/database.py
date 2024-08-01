#database.py
import logging
from databases import Database
from sqlalchemy import create_engine, MetaData
import os

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv('DATABASE_URL', "DATABASEURL")

engine = create_engine(DATABASE_URL)
metadata = MetaData()

database = Database(DATABASE_URL)
