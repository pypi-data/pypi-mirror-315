from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Password:
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def check_password(password: str, hashed_password: str) -> bool:
        return pwd_context.verify(password, hashed_password)
