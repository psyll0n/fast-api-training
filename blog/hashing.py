from passlib.context import CryptContext


class Hash:
    def __init__(self, hash_type: str):
        self.hash_type = hash_type

    def bcrrypt(password: str) -> str:
        """
        Hash a password using bcrypt.
        """
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        # Create a new user instance with the hashed password
        hashed_password = pwd_context.hash(password)

        return pwd_context.hash(password)
