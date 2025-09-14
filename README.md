# Have I Been Pwned - Flask

A personal security monitoring system that periodically checks email addresses for data breaches using the Have I Been Pwned API.

## Features

- **Single-user system** with JWT authentication
- **Email monitoring** - Add multiple email addresses to monitor
- **Automated breach checking** - Configurable scheduled checks 
- **Web dashboard** - Modern UI for managing emails, viewing breaches, and settings
- **Real-time notifications** - Get alerted when new breaches are found
- **RESTful API** - Complete API for all functionality

## Architecture

- **Backend**: Flask with SQLAlchemy
- **Frontend**: Bootstrap 5 with Jinja2 templates  
- **Authentication**: JWT tokens
- **Database**: SQLite
- **Scheduler**: APScheduler for automated checks
- **API Integration**: Have I Been Pwned API

---

## API Documentation

### Authentication

All API endpoints (except login page and registration) require JWT authentication.

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

### Standard Response Format

All API responses follow this structure:

```json
{
  "success": boolean,
  "message": string,
  "data": object | null,
  "error": string | null
}
```

---

## API Endpoints

### 🔐 Authentication & User Management

#### GET `/api/user/login-page`
Renders the login/registration page.
- **Authentication**: None required
- **Returns**: HTML page (login form if user exists, registration form if no user)

#### GET `/api/user/dashboard`  
Renders the main dashboard.
- **Authentication**: None required (checked on frontend)
- **Returns**: HTML dashboard page

#### POST `/api/user/register`
Register a new user account.
- **Authentication**: None (only works if no user exists)
- **Body**:
```json
{
  "user_name": "string",
  "email": "string", 
  "password": "string"
}
```
- **Returns**: Success confirmation
- **Status Codes**: 200 (success), 409 (user exists), 422 (validation error)

#### POST `/api/user/login`
Login with user credentials.
- **Authentication**: None required
- **Body**:
```json
{
  "email": "string",
  "password": "string"
}
```
- **Returns**: 
```json
{
  "success": true,
  "data": {
    "access_token": "jwt_token_string"
  }
}
```
- **Status Codes**: 200 (success), 422 (validation error)

#### POST `/api/user/change_password`
Change user password.
- **Authentication**: JWT required  
- **Body**:
```json
{
  "user_name": "string",
  "password": "new_password"
}
```
- **Returns**: Success confirmation
- **Status Codes**: 200 (success), 422 (validation error)

---

### 📧 Email Management

#### GET `/api/email`
Get all monitored email addresses.
- **Authentication**: JWT required
- **Returns**:
```json
{
  "success": true,
  "data": {
    "emails": [
      {
        "id": 1,
        "email": "user@example.com"
      }
    ]
  }
}
```

#### POST `/api/email`
Add a new email address to monitor.
- **Authentication**: JWT required
- **Body**:
```json
{
  "email": "new@example.com"
}
```
- **Returns**: Success confirmation with added email
- **Status Codes**: 200 (success), 400 (already exists), 422 (validation error)

#### DELETE `/api/email/<id>`
Delete a specific email address.
- **Authentication**: JWT required
- **Path Parameters**: `id` (integer) - Email ID
- **Returns**: Success confirmation
- **Status Codes**: 200 (success), 400 (not found)

#### DELETE `/api/email/all`
Delete all monitored email addresses.
- **Authentication**: JWT required
- **Returns**: Success confirmation
- **Status Codes**: 200 (success), 400 (error)

---

### 🔓 Breach Information

#### GET `/api/pwned_platforms`
Get all detected breaches across all emails.
- **Authentication**: JWT required
- **Returns**:
```json
{
  "success": true,
  "data": {
    "platforms": [
      {
        "id": 1,
        "email_id": 1,
        "name": "Adobe",
        "title": "Adobe", 
        "domain": "adobe.com",
        "breach_date": "2013-10-04",
        "added_date": "2013-12-04T00:00:00",
        "description": "Breach description...",
        "is_verified": true,
        "data_classes": ["Email addresses", "Passwords"],
        "created_at": "2024-01-01T00:00:00"
      }
    ]
  }
}
```

#### GET `/api/pwned_platforms/email/<email_id>`
Get breaches for a specific email address.
- **Authentication**: JWT required
- **Path Parameters**: `email_id` (integer) - Email ID
- **Returns**: Same format as above, filtered by email

#### DELETE `/api/pwned_platforms`
Delete all breach records (for testing purposes).
- **Authentication**: JWT required
- **Returns**: Success confirmation
- **Status Codes**: 200 (success), 400 (error)

---

### ⚙️ Scheduler Settings

#### GET `/api/scheduler/settings`
Get current breach checking schedule settings.
- **Authentication**: JWT required
- **Returns**:
```json
{
  "success": true,
  "data": {
    "interval_unit": "hours",
    "interval_value": 1
  }
}
```

#### PUT `/api/scheduler/settings`
Update breach checking schedule.
- **Authentication**: JWT required
- **Body**:
```json
{
  "interval_unit": "hours",
  "interval_value": 6
}
```
- **Valid units**: "seconds", "minutes", "hours", "days"
- **Valid values**: Any positive integer
- **Returns**: Success confirmation
- **Status Codes**: 200 (success), 400 (invalid settings), 422 (validation error)

#### GET `/api/scheduler/status`
Get current scheduler job status.
- **Authentication**: JWT required
- **Returns**:
```json
{
  "success": true,
  "data": {
    "jobs": [
      {
        "id": "pwn_check_job",
        "name": "Check for new breaches",
        "next_run_time": "2024-01-01T12:00:00",
        "trigger": "interval[0:01:00]"
      }
    ]
  }
}
```

---

### 🏠 Utility Endpoints (Development)

#### GET `/`
Simple hello world endpoint.
- **Authentication**: None required
- **Returns**: HTML "Hello World!" message

#### GET `/<name>`
Echo the provided name.
- **Authentication**: None required  
- **Path Parameters**: `name` (string)
- **Returns**: The provided name as plain text

#### GET `/create_dummy_user`
Create a dummy user for testing.
- **Authentication**: None required
- **Returns**: Confirmation message

#### GET `/get_dummy_user`
Get dummy user information.
- **Authentication**: None required
- **Returns**: Dummy user details

#### GET `/all_users`
Get all users (development endpoint).
- **Authentication**: None required
- **Returns**: All user information

---

## Data Models

### User Model
```json
{
  "id": integer,
  "user_name": "string",
  "email": "string", 
  "password": "string (hashed)",
  "created_at": "datetime"
}
```

### Email Model
```json
{
  "id": integer,
  "user_id": integer,
  "email": "string",
  "created_at": "datetime"
}
```

### Breach (PwnedPlatform) Model
```json
{
  "id": integer,
  "email_id": integer,
  "name": "string",
  "title": "string",
  "domain": "string",
  "breach_date": "date",
  "added_date": "datetime",
  "description": "string",
  "is_verified": boolean,
  "data_classes": ["array of strings"],
  "created_at": "datetime"
}
```

### Scheduler Config Model
```json
{
  "id": integer,
  "key": "string",
  "value": "string", 
  "updated_at": "datetime"
}
```

---

## Error Handling

### Common HTTP Status Codes

- **200**: Success
- **400**: Bad request / Operation failed
- **401**: Unauthorized / No token / Session expired
- **409**: Conflict (user already exists)
- **422**: Validation error (invalid JSON format)
- **500**: Internal server error

### Error Response Example
```json
{
  "success": false,
  "message": "User already exists", 
  "data": null,
  "error": "Detailed error information"
}
```

---

## Rate Limiting

The system implements a 15-second delay between checking each email address to respect the Have I Been Pwned API rate limits.

---

## Security Features

- **JWT Authentication** for all protected endpoints
- **Single-user system** - prevents unauthorized account creation
- **Input validation** using Pydantic models
- **SQL injection protection** via SQLAlchemy ORM
- **Password hashing** for user credentials
- **Request logging** with IP tracking

---

## TODO

- [x] Implement DB Repositories on top of Flask-SQLAlchemy
- [x] Implement user account registration with Flask-JWT Extended
- [x] Implement Flask Cronjob for have-i-been-pwned requests
- [x] Handle pydantic exception in router layer
- [x] Create comprehensive API documentation
- [ ] Implement swagger documentation for the API
- [ ] Implement custom data models for repository returns
- [ ] Learn SQLAlchemy Exceptions, divide them into custom exceptions
- [ ] Detail the exception handlers at the router layer
