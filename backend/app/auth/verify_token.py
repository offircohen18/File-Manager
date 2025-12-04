from fastapi import HTTPException, Header
import firebase_admin
from firebase_admin import auth, credentials

# Initialize Firebase once
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

def verify_token(authorization: str = Header(...)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")
    
    token = authorization.replace("Bearer", "").strip()
    
    try:
        decoded = auth.verify_id_token(token)
        # Make sure 'role' exists, default to 'user'
        if "role" not in decoded:
            decoded["role"] = "user"
        return decoded
    except auth.ExpiredIdTokenError:
        raise HTTPException(status_code=401, detail="Token expired")
    except auth.InvalidIdTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token verification error: {str(e)}")
