from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db(app):
    try:
        client = MongoClient(app.config['MONGO_URI'], serverSelectionTimeoutMS=30000)
        client.admin.command('ping')  
        db = client.get_database('user_db')
        logger.info("Connected to MongoDB")
        app.db = db  
        return db
    except ConnectionFailure as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise