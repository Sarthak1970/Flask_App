from bson import ObjectId
from pymongo.errors import DuplicateKeyError
import bcrypt
import logging
from app.models.user import User

logger = logging.getLogger(__name__)

def create_user(db, user_data: User):
    try:
        # Hash password
        hashed_password = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt())
        user_dict = user_data.dict(exclude_unset=True)
        user_dict['password'] = hashed_password.decode('utf-8')
        
        # Ensure email is unique
        db.users.create_index("email", unique=True)
        
        # Insert user
        result = db.users.insert_one(user_dict)
        user_dict['_id'] = str(result.inserted_id)
        return user_dict
    except DuplicateKeyError:
        logger.error(f"User with email {user_data.email} already exists")
        raise ValueError(f"User with email {user_data.email} already exists")
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise

def get_all_users(db):
    try:
        users = list(db.users.find())
        for user in users:
            user['_id'] = str(user['_id'])
            user.pop('password', None)  # Remove password from response
        return users
    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        raise

def get_user_by_id(db, user_id: str):
    try:
        user = db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            logger.error(f"User with ID {user_id} not found")
            raise ValueError(f"User with ID {user_id} not found")
        user['_id'] = str(user['_id'])
        user.pop('password', None)
        return user
    except Exception as e:
        logger.error(f"Error fetching user {user_id}: {e}")
        raise

def update_user(db, user_id: str, user_data: User):
    try:
        user_dict = user_data.dict(exclude_unset=True)
        if 'password' in user_dict:
            user_dict['password'] = bcrypt.hashpw(user_dict['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        result = db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": user_dict}
        )
        if result.matched_count == 0:
            logger.error(f"User with ID {user_id} not found")
            raise ValueError(f"User with ID {user_id} not found")
        return get_user_by_id(db, user_id)
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {e}")
        raise

def delete_user(db, user_id: str):
    try:
        result = db.users.delete_one({"_id": ObjectId(user_id)})
        if result.deleted_count == 0:
            logger.error(f"User with ID {user_id} not found")
            raise ValueError(f"User with ID {user_id} not found")
        return {"message": f"User with ID {user_id} deleted"}
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {e}")
        raise