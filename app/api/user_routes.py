from flask import Blueprint, request, jsonify
from app.models.user import User
from app.services.user_service import create_user, get_all_users, get_user_by_id, update_user, delete_user
import logging

logger = logging.getLogger(__name__)
users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['GET'])
def get_users():
    try:
        users = get_all_users(request.app.db)
        return jsonify({"status": "success", "data": users})
    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@users_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = get_user_by_id(request.app.db, user_id)
        return jsonify({"status": "success", "data": user})
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 404
    except Exception as e:
        logger.error(f"Error fetching user {user_id}: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@users_bp.route('/users', methods=['POST'])
def create_new_user():
    try:
        user_data = User(**request.get_json())
        user = create_user(request.app.db, user_data)
        return jsonify({"status": "success", "data": user}), 201
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@users_bp.route('/users/<user_id>', methods=['PUT'])
def update_existing_user(user_id):
    try:
        user_data = User(**request.get_json())
        user = update_user(request.app.db, user_id, user_data)
        return jsonify({"status": "success", "data": user})
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 404
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@users_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_existing_user(user_id):
    try:
        result = delete_user(request.app.db, user_id)
        return jsonify({"status": "success", "data": result})
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 404
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500