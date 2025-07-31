import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class Config:
    def __init__(self):
        self.MONGO_URI = os.getenv("MONGO_URI")
        self.FLASK_ENV = os.getenv("FLASK_ENV", "development")
        
        if not self.MONGO_URI:
            logger.error("MONGO_URI is not set in .env file")
            raise ValueError("MONGO_URI must be set in .env file")
        if not self.FLASK_ENV:
            logger.warning("FLASK_ENV is not set, defaulting to 'development'")

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False