from datetime import datetime, timedelta
import jwt

SECRET_KEY = "SECRET"
ALGORITHM = "HS256"

def create_reset_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_reset_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])