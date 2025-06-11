from . import schemas
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from .schemas import TokenData

# blog/token.py


SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    """
    Create a new access token.

    Args:
        data (dict): The data to include in the token.
        expires_delta (timedelta, optional): The expiration time for the token. Defaults to timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES).

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Add the expiration time to the token data
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    # Return the encoded JWT token
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    """
    Verify the provided JWT token.

    Args:
        token (str): The JWT token to verify.

    Returns:
        dict: The decoded token data if verification is successful.

    Raises:
        JWTError: If the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError as e:
        raise e