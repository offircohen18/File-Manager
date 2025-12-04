import firebase_admin
from firebase_admin import auth, credentials

# Initialize Firebase (only once)
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

# Replace with the UID of the user you want to make admin
uid = "HEcthVCyNKaGvCrhyc9FPl2wbbr2"

auth.set_custom_user_claims(uid, {"role": "admin"})
print(f"Admin role assigned to user {uid}")
