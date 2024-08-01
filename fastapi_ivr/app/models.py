# models.py
import sqlalchemy
from .database import metadata

user_interactions = sqlalchemy.Table(
    "user_interactions",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.String),
    sqlalchemy.Column("message", sqlalchemy.String),
    sqlalchemy.Column("response", sqlalchemy.String),
    sqlalchemy.Column("timestamp", sqlalchemy.DateTime),
    sqlalchemy.Column("call_duration", sqlalchemy.Integer, nullable=True),
    sqlalchemy.Column("call_sid", sqlalchemy.String)
)

customers = sqlalchemy.Table(
    "customers",
    metadata,
    sqlalchemy.Column("phone_number", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("customer_name", sqlalchemy.String),  
    sqlalchemy.Column("customer_address", sqlalchemy.String),
    sqlalchemy.Column("customer_zipcode", sqlalchemy.String)
)

issues = sqlalchemy.Table(
    "issues",
    metadata,
    sqlalchemy.Column("issue_id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("phone_number", sqlalchemy.String),
    sqlalchemy.Column("issue_description", sqlalchemy.String),
    sqlalchemy.Column("location", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("status", sqlalchemy.String, default="open"),
    sqlalchemy.Column("issue_start_date", sqlalchemy.DateTime),
    sqlalchemy.Column("issue_expected_date", sqlalchemy.String),
    sqlalchemy.Column("issue_solved_date", sqlalchemy.DateTime),
)
