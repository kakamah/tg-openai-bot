# Hello World Django API with Login

A simple Django project with a REST API that includes basic login functionality using Django REST Framework.

## Setup

The project is already set up with:
- Python virtual environment (`.venv`)
- Django 4.2.30
- Django REST Framework 3.16.1
- Token-based authentication

## Running the Server

```bash
source .venv/bin/activate
python manage.py runserver
```

The server will be available at `http://localhost:8000/`

## API Endpoints

### 1. Login
**POST** `/api/login/`

Request:
```json
{
  "username": "testuser",
  "password": "testpass123"
}
```

Response:
```json
{
  "token": "your-auth-token",
  "user_id": 1,
  "username": "testuser"
}
```

### 2. Hello World
**GET** `/api/hello/`

Requires authentication header:
```
Authorization: Token your-auth-token
```

Response:
```json
{
  "message": "Hello, World!",
  "user": "testuser"
}
```

## Test Credentials

- **Username**: `testuser`
- **Password**: `testpass123`

## Testing with curl

```bash
# Login
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'

# Use the returned token to call the hello endpoint
curl -X GET http://localhost:8000/api/hello/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

## Admin Panel

Access the Django admin at `/admin/` with superuser credentials.

To create a superuser:
```bash
python manage.py createsuperuser
```
