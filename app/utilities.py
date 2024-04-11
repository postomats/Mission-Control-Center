import jwt
from fastapi import HTTPException
from .SETTINGS import JWT_KEY, USER_APP_IP
import requests

def get_user_id_from_token(jwt_token: str):
    try:
        payload = jwt.decode(jwt_token, JWT_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    

def is_worker(jwt):
    url = f"http://127.0.0.1:8001/me?token={jwt}"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise HTTPException(status_code=403, detail="Failed to authenticate user")
    
    user_data = response.json()
    role = user_data.get("role")
    
    if role not in ["Worker", "Admin"]:
        raise HTTPException(status_code=403, detail="You don't have permission to process this order")
    return True

