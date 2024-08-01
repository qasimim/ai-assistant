# crud.py
import logging
from sqlalchemy import select, update, insert
from ..models import customers
from ..database import database

logger = logging.getLogger(__name__)

async def check_and_update_or_create_customer(phone_number, customer_name, customer_zipcode, customer_address):
    query = select([customers]).where(customers.c.phone_number == phone_number)
    customer = await database.fetch_one(query)
    try:
        if customer:
            logger.info(f"Updating customer {phone_number}")
            query = (
                update(customers).
                where(customers.c.phone_number == phone_number).
                values(customer_name=customer_name, customer_zipcode=customer_zipcode, customer_address=customer_address)
            )
        else:
            logger.info(f"Creating customer {phone_number}")
            query = (
                insert(customers).
                values(phone_number=phone_number, customer_name=customer_name, customer_zipcode=customer_zipcode, customer_address=customer_address)
            )
        await database.execute(query)
    except Exception as e:
        logger.error(f"Error with database operation for customer {phone_number}: {e}", exc_info=True)
        raise
