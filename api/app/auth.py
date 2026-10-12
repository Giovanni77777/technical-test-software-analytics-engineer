import jwt
from fastapi import Header, HTTPException

SECRET_KEY = "rdp-dev-secret-change-me"


def get_current_user(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"email": payload["sub"], "studies": payload.get("studies", [])}
