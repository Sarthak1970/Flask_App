# flask_user_api/app/__init__.py
from flask import Flask
from config import DevelopmentConfig
from app.database.db import init_db
from app.api.user_routes import users_bp
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    
    try:
        config = DevelopmentConfig()
        app.config['MONGO_URI'] = config.MONGO_URI
        app.config['FLASK_ENV'] = config.FLASK_ENV
        app.config['DEBUG'] = config.DEBUG
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        raise

    try:
        init_db(app)
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

    app.register_blueprint(users_bp)

    @app.route('/')
    def hello():
        return {"message": "Flask User API is running!"}

    return app

app = create_app()