from sqlalchemy.ext.asyncio import AsyncSession
from base_lib.interactor.schema.base_schemas import TokenData
from base_lib.configs.config import settings
import bcrypt
import jwt
from typing import Optional

# Configuration values
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS


async def verify_token(token: str, db: AsyncSession) -> Optional[TokenData]:
    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username_or_email: str = payload.get("sub")

        if username_or_email is None:
            return None

        return TokenData(username_or_email=username_or_email)
    except Exception:
        # Handle invalid or expired tokens
        return None


def get_password_hash(password: str) -> str:
    hashed_password: str = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    return hashed_password
