# 📝 Django Todo API

A clean and simple REST API for task management built with Django REST Framework.

## ✨ Features

- 🔐 **User Authentication** (JWT-based)
- 📋 **CRUD Operations** for tasks
- ✅ **Task Status Management** (New, Active, Done)
- 🔍 **Filter Tasks** by status
- 👥 **User-specific Tasks** (privacy protection)
- 🔧 **Admin Panel** access for superusers

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL

### Installation

1. **Clone & Setup**
   ```bash
   git clone https://github.com/murad48oguz/andersentechtask
   cd django-todo-api
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**
   ```bash
   pip install django djangorestframework djangorestframework-simplejwt
   pip install django-cors-headers psycopg2-binary
   ```

3. **Database Setup**
   ```sql
   CREATE DATABASE tododb;
   CREATE USER todouser WITH PASSWORD 'passTodo@777!!!';
   GRANT ALL PRIVILEGES ON DATABASE tododb TO todouser;
   ```

4. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser  # Optional
   python manage.py runserver
   ```

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api/
```

### 🔑 Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/register/` | Register new user |
| `POST` | `/token/` | Login & get JWT tokens |
| `POST` | `/token/refresh/` | Refresh access token |

### 📋 Task Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/tasks/` | List user's tasks |
| `POST` | `/tasks/` | Create new task |
| `GET` | `/tasks/{id}/` | Get specific task |
| `PUT` | `/tasks/{id}/` | Update task |
| `DELETE` | `/tasks/{id}/` | Delete task |
| `POST` | `/tasks/{id}/complete/` | Mark task as done |

### 🔍 Query Parameters
- `?status=New` - Filter by status (New, Active Task, Done)
- `?page=2` - Pagination

## 💡 Usage Examples

### 1. Register User
```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "username": "john",
    "password": "securepass123"
  }'
```

### 2. Login
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepass123"
  }'
```

### 3. Create Task
```bash
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn Django",
    "description": "Complete Django REST API tutorial",
    "status": "New"
  }'
```

### 4. Get Tasks
```bash
curl -X GET http://localhost:8000/api/tasks/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 5. Mark Task Complete
```bash
curl -X POST http://localhost:8000/api/tasks/1/complete/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 📊 Data Models

### User
```python
{
  "email": "john@example.com",
  "username": "john",
  "first_name": "John",
  "last_name": "Doe"
}
```

### Task
```python
{
  "id": 1,
  "title": "Task Title",
  "description": "Task description",
  "status": "New",  # New, Active Task, Done
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:00:00Z"
}
```

## 🔐 Authentication

The API uses **JWT (JSON Web Tokens)** for authentication.

### Token Lifecycle
- **Access Token**: 60 minutes
- **Refresh Token**: 1 day

### How to Use
Include the token in request headers:
```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Login Options
You can login with either:
- Email address
- Username

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

Tests cover:
- User registration/login
- Task CRUD operations
- Permissions
- Status filtering

## 🔒 Security Features

- ✅ JWT token authentication
- ✅ Password validation (min 6 chars)
- ✅ User-specific data access
- ✅ CORS protection
- ✅ Admin role separation

## 🛠️ Tech Stack

- **Backend**: Django 4.2.23
- **API**: Django REST Framework
- **Auth**: Simple JWT
- **Database**: PostgreSQL
- **CORS**: django-cors-headers

## 📁 Project Structure

```
django-todo-api/
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── tasks/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── permissions.py
│   ├── authentication.py
│   ├── urls.py
│   └── tests.py
└── manage.py
```

## 🚨 Important Notes

- **Development**: `DEBUG = True` (change for production)
- **CORS**: Currently allows all origins (restrict for production)
- **Database**: Update credentials in `settings.py`
- **Secret Key**: Change in production
