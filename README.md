# Flask User API🚀

A scalable Flask REST API for performing CRUD operations on a User resource stored in MongoDB, built with Docker, tested with pytest and Postman, and deployed on Render. The project follows modern system design principles to ensure scalability, maintainability, and robustness.

---

## Features

- REST API endpoints for Create, Read, Update, Delete (CRUD) operations on Users.
- User fields: `id` (MongoDB ObjectId), `name`, `email`, `password` (hashed with bcrypt).
- Modular structure with separated concerns for database, models, services, and routes.
- Environment-based configuration using `.env`.
- Comprehensive unit tests using `pytest`.
- Manual testing with Postman.
- Logging and error handling for production readiness.
- Deployed on Render with MongoDB for scalability.

---

## System Design Techniques 🛠️

### Modular Architecture

- Separated concerns into distinct layers:
  - Database: `app/database/db.py`
  - Models: `app/models/user.py`
  - Services: `app/services/user_service.py`
  - Routes: `app/api/user_routes.py`
- **Benefits**: Enhances code maintainability, testability, and scalability by isolating business logic, data access, and API endpoints.

### Environment-Based Configuration

- Uses `python-dotenv` and `config.py` to load environment variables (`FLASK_ENV`, `MONGO_URI`, `SECRET_KEY`) from `.env`.
- Supports `DevelopmentConfig` and `ProductionConfig` for different environments.
- **Benefits**: Ensures portability and security by avoiding hardcoded values, suitable for local and cloud deployments.

### Input Validation with Pydantic

- Employs Pydantic (`app/models/user.py`) for request body validation with strict typing and email format checks.
- **Benefits**: Prevents invalid data from entering the system, improving reliability and security.

### Password Security

- Uses `bcrypt` to hash passwords before storing in MongoDB.
- **Benefits**: Enhances security by protecting user credentials against breaches.

### Database Isolation for Testing

- Uses a separate test database (`test_user_db`) during `pytest` runs to avoid conflicts with the production database (`user_db`).
- **Benefits**: Ensures test reliability and prevents accidental data modification in production.

### Error Handling and Logging

- Structured error handling in `user_routes.py` (`400`, `404`, `500`).
- Uses Python’s `logging` module.
- **Benefits**: Improves debugging and operational reliability in production.

### Dockerization

- Dockerized with `Dockerfile` and `docker-compose.yml` for optional deployment.
- **Benefits**: Simplifies deployment, ensures consistency across environments, and supports scaling on platforms like Render.

### Unique Constraints

- MongoDB unique index on email to prevent duplicate users.
- **Benefits**: Enforces data integrity at the database level.

### RESTful Design

- Follows REST principles with clear endpoint semantics (`GET`, `POST`, `PUT`, `DELETE`) and JSON responses.
- **Benefits**: Enhances API usability and interoperability.

### Production Readiness

- Uses `gunicorn` for production-grade WSGI server.
- Configurable `SECRET_KEY` for security.
- **Benefits**: Ensures performance and security in production environments.

---

## Setup

### Clone the Repository

```bash
git clone <your-repo-url>
cd flask_user_api
```

### Create `.env` File

```bash
cp .env.example .env
```

Update `.env` with:

```env
FLASK_ENV=development
MONGO_URI=mongodb://localhost:27017/user_db
```

> ⚠️ Make sure MongoDB is running locally on your machine. Default URI points to `localhost`.

### Run Locally (Without Docker)

```bash
# 1. Create and activate a virtual environment
python -m venv myenv
source myenv/bin/activate  # Windows: myenv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set environment variables (if not using .env)
export FLASK_ENV=development
export FLASK_APP=app

# 4. Run the app
flask run
```

Your API will be available at: [http://localhost:5000](http://localhost:5000)

---

## Testing Tutorial

### Unit Testing with `pytest`

Make sure MongoDB is running locally.

```bash
source myenv/bin/activate  # Windows: myenv\Scripts\activate
pytest -v
```

- Tests located in `tests/test_users.py`
- Uses separate `test_user_db`
- Fixtures: `client`, `clear_db`, `user_id`
- Covers: `/`, `/users`, `/users/<id>`

Save test output:

```bash
pytest -v > test_output.txt
```

---

## Manual Testing with Postman

Start the app:

```bash
flask run
```

### Test Cases

#### `GET /`
```http
GET http://localhost:5000/
Expected: 200 OK
```

#### `POST /users`
```http
POST http://localhost:5000/users
Headers: Content-Type: application/json
Body:
{
  "name": "Test User",
  "email": "test.user.unique16@example.com",
  "password": "securepassword"
}
```

Copy `_id` from response.

#### `GET /users`
```http
GET http://localhost:5000/users
```

#### `GET /users/<id>`
```http
GET http://localhost:5000/users/<your_id>
```

#### `PUT /users/<id>`
```http
PUT http://localhost:5000/users/<your_id>
Headers: Content-Type: application/json
Body:
{
  "name": "Updated User",
  "email": "updated.user16@example.com",
  "password": "newpassword"
}
```

#### `DELETE /users/<id>`
```http
DELETE http://localhost:5000/users/<your_id>
```

---

## Project Structure

```
flask_user_api/
├── app/
│   ├── __init__.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── db.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── user_routes.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── user_service.py
├── tests/
│   ├── __init__.py
│   └── test_users.py
├── config.py
├── .env
├── .env.example
├── requirements.txt
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── README.md
```

---

## 🐳 Optional: Run with Docker (if preferred)

```bash
docker-compose up --build
```

This will start both Flask and MongoDB in Docker containers.

API will be available at: [http://localhost:5000](http://localhost:5000)

