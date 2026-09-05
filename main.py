import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from supabase import create_client, Client
from dotenv import load_dotenv
from middleware.auth import require_auth

# ========================================================
# App & Supabase setup
# ========================================================
# Equivalent to require("dotenv").config()
load_dotenv()

app = FastAPI()

# Initialize Supabase client
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# Security scheme to extract Bearer tokens
security = HTTPBearer()

# Request body schema (Equivalent to Express req.body destructuring)
class UserCredentials(BaseModel):
    email: str
    password: str

# # ==========================================================================
# # Middleware: require_auth
# # Verifies the "Authorization: Bearer <token>" header against Supabase.
# # ==========================================================================
# def require_auth(credentials: HTTPAuthorizationCredentials = Depends(security)):
#     token = credentials.credentials
#     if not token:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Access token required",
#         )
        
#     try:
#         # Ask Supabase to validate the token and return the associated user
#         response = supabase.auth.get_user(token)
#         if not response.user:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid or expired token"
#             )
#         return response.user
#     except Exception:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, 
#             detail="Invalid or expired token"
#         )

# ==========================================================================
# POST /auth/signup
# Creates a new user account via Supabase Auth.
# ==========================================================================
@app.post("/auth/signup", status_code=status.HTTP_201_CREATED)
def signup(creds: UserCredentials):
    try:
        res = supabase.auth.sign_up({
            "email": creds.email, 
            "password": creds.password
        })
        return {"user": res.user}
    except Exception as e:
        # Supabase raises an exception on error in the Python client
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e)
        )

# ==========================================================================
# POST /auth/login
# Authenticates an existing user and returns session tokens.
# ==========================================================================
@app.post("/auth/login", status_code=status.HTTP_200_OK)
def login(creds: UserCredentials):
    try:
        res = supabase.auth.sign_in_with_password({
            "email": creds.email, 
            "password": creds.password
        })
        return {
            "access_token": res.session.access_token,
            "refresh_token": res.session.refresh_token,
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid login credentials"
        )

# ==========================================================================
# GET /public/info
# A route anyone can access, no auth required.
# ==========================================================================
@app.get("/public/info", status_code=status.HTTP_200_OK) 
def public_info(): 
    return {"message": "Welcome stranger! This info is public."}

# ==========================================================================
# GET /protected/profile
# Requires a valid Bearer token (checked by require_auth).
# ==========================================================================
@app.get("/protected/profile", status_code=status.HTTP_200_OK)
def protected_profile(user = Depends(require_auth)):
    return {
        "id": user.id,
        "email": user.email,
        "accountCreated": user.created_at,
    }
    
# ==========================================================================
# GET /protected/dashboard
# Another protected route using the SAME require_auth dependency.
# ==========================================================================

@app.get("/protected/dashboard", status_code=status.HTTP_200_OK)
def protected_dashboard(user=Depends(require_auth)):
    return {
        "message": "Welcome to your dashboard!",
        "id": user.id,
        "email": user.email,
    }


# ==========================================================================
# POST /auth/logout
# Protected route. Signs the user out through Supabase.
# ==========================================================================

@app.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(user=Depends(require_auth)):
    try:
        supabase.auth.sign_out()
        return None
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed"
        )      