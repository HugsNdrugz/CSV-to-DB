import os
from models import get_db_connection
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def insert_test_data():
    """Insert test messenger data into the chats table"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Sample chat messages
                messages = [
                    ('John Doe', 'Hello there!', datetime.now() - timedelta(hours=2)),
                    ('Alice Smith', 'Hi! How are you?', datetime.now() - timedelta(hours=1)),
                    ('John Doe', 'I am doing great!', datetime.now() - timedelta(minutes=45)),
                    ('Bob Wilson', 'Meeting at 3?', datetime.now() - timedelta(minutes=30)),
                    ('Alice Smith', 'Yes, that works!', datetime.now() - timedelta(minutes=15))
                ]
                
                # Insert messages using a single statement
                for sender, text, time in messages:
                    cur.execute(
                        "INSERT INTO chats (sender, text, time) VALUES (%s, %s, %s)",
                        (sender, text, time)
                    )
                
                logger.info("Test data inserted successfully!")
                
    except Exception as e:
        logger.error(f"Error inserting test data: {str(e)}")
        raise

if __name__ == '__main__':
    insert_test_data()