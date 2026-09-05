# Build a secure API with Supabase Auth (FastAPI)

### Authentication Flow

```mermaid
sequenceDiagram
    participant Client
    participant FastAPI
    participant Supabase

    Note over Client,Supabase: 1. Authentication
    Client->>FastAPI: POST /auth/login (email, password)
    FastAPI->>Supabase: sign_in_with_password()
    Supabase-->>FastAPI: Session (access_token, refresh_token)
    FastAPI-->>Client: Returns tokens

    Note over Client,Supabase: 2. Accessing Protected Routes
    Client->>FastAPI: GET /protected/profile (Bearer Token)
    FastAPI->>Supabase: get_user(token)
    Supabase-->>FastAPI: Validates & returns user data
    FastAPI-->>Client: Returns 200 OK (User Profile)

```

### Python Environment Setup

```bash
# Update package list and install Python 3 & pip (Debian/Ubuntu example)
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Verify the Python version:
python3 --version # Should print Python 3.x

# Create an isolated virtual environment for the project:
python3 -m venv venv

# Activate the virtual environment:
source venv/bin/activate

```

### Server start

**Install the required packages**

```bash
pip install -r requirements.txt

```

**Run your server**

```bash
uvicorn main:app --port 3000 --reload

```

### SignUp

```bash
curl -i -X POST http://localhost:3000/auth/signup \
-H "Content-Type: application/json" \
-d '{"email":"test@example.com","password":"password123"}'

```

### login

```bash
curl -i -X POST http://localhost:3000/auth/login \
-H "Content-Type: application/json" \
-d '{"email":"test@example.com","password":"password123"}'

```

### Public Gate

```bash
curl -i http://localhost:3000/public/info

```

It should output `200`

### Protected Gate

```bash
curl -i http://localhost:3000/protected/profile

```

It should give error 401 `{"error":"Access token required"}`

### Protected Gate with token
```bash
curl -i http://localhost:3000/protected/profile \
  -H "Authorization: Bearer PASTE_ACCESS_TOKEN_HERE"
```
### Logout
```bash
curl -X POST http://localhost:3000/auth/logout \
  -H "Authorization: Bearer PASTE_ACCESS_TOKEN_HERE" 
```
### Swagger UI photo

![SwaggerUI](SwaggerUI.png)
