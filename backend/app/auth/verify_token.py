from fastapi import HTTPException, Header
from firebase_admin import auth
from app.firebase import init_firebase

init_firebase()

def verify_token(authorization: str = Header(...)) -> dict:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")
    
    token_str = authorization.replace("Bearer", "").strip()
    
    try:
        decoded = auth.verify_id_token(token_str)
        if "role" not in decoded:
            decoded["role"] = "user"
        return decoded
    except auth.ExpiredIdTokenError:
        raise HTTPException(status_code=401, detail="Token expired")
    except auth.InvalidIdTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token verification error: {str(e)}")
