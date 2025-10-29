from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings

oAuthBearer = OAuth2PasswordBearer(tokenUrl="token")

def create_token(citizen_id: str):
    to_encode = {}
    hash_id = settings.cryptContext.hash(citizen_id)
    to_encode.update({"sub": hash_id})
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encode = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encode

def verify_token(token, citizen_id):
    try:
        code = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHIM])
        id = code.get("sub")
        if settings.cryptContext.verify(citizen_id, id):
            return True, ""
        return False, "Token không chính xác"
    except ExpiredSignatureError:
        return False, "Token hết hạn"
    except JWTError:
        return False, "Token không có quyền hạn"