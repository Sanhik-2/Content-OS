
import os
import json
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

# Configuration
SECRET_KEY = os.getenv("AUTH_SECRET_KEY", "super_secret_ai_key_change_me_in_prod")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 24 * 60 # 30 days for this local tool
USERS_DB_PATH = "security_data/users.json"

# Password Hashing
# Switched to argon2 to avoid bcrypt's 72 byte limit and compatibility issues
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Models ---
class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    role: str = "creator" # creator, admin

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# --- User Database Simulation ---
def ensure_db():
    if not os.path.exists("security_data"):
        os.makedirs("security_data")
    if not os.path.exists(USERS_DB_PATH):
        # Create default admin user: admin / admin123
        hashed_pw = pwd_context.hash("admin123")
        default_users = {
            "admin": {
                "username": "admin",
                "email": "admin@contentos.ai",
                "full_name": "System Admin",
                "hashed_password": hashed_pw,
                "disabled": False,
                "role": "admin"
            }
        }
        with open(USERS_DB_PATH, "w") as f:
            json.dump(default_users, f, indent=4)

def get_user(username: str):
    ensure_db()
    with open(USERS_DB_PATH, "r") as f:
        users = json.load(f)
    if username in users:
        return UserInDB(**users[username])
    return None

def create_user(user_data: Dict[str, Any]):
    ensure_db()
    with open(USERS_DB_PATH, "r") as f:
        users = json.load(f)
    
    username = user_data["username"]
    if username in users:
        return False, "User already exists"
    
    user_data["hashed_password"] = pwd_context.hash(user_data["password"])
    del user_data["password"]
    
    users[username] = user_data
    with open(USERS_DB_PATH, "w") as f:
        json.dump(users, f, indent=4)
    return True, "User created"

# --- Authentication Logic ---
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_01_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
