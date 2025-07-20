from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from typing import Optional
import firebase_admin
from firebase_admin import auth, credentials

router = APIRouter()
security = HTTPBearer()

class UserSignup(BaseModel):
    email: str
    password: str
    display_name: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict

@router.post("/signup", response_model=TokenResponse)
async def signup(user_data: UserSignup):
    """Create a new user account"""
    try:
        # Create user in Firebase
        user = auth.create_user(
            email=user_data.email,
            password=user_data.password,
            display_name=user_data.display_name
        )
        
        # Generate custom token
        custom_token = auth.create_custom_token(user.uid)
        
        return TokenResponse(
            access_token=custom_token.decode('utf-8'),
            token_type="bearer",
            user={
                "uid": user.uid,
                "email": user.email,
                "display_name": user.display_name
            }
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login(user_data: UserLogin):
    """Login user (client-side Firebase Auth)"""
    # Note: This is typically handled on the frontend with Firebase SDK
    # This endpoint can be used for additional server-side validation
    return {"message": "Use Firebase Auth SDK on frontend for login"}

@router.post("/verify-token")
async def verify_token(token: str = Depends(security)):
    """Verify Firebase ID token"""
    try:
        decoded_token = auth.verify_id_token(token.credentials)
        return {"valid": True, "user_id": decoded_token["uid"]}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/user-profile")
async def get_user_profile(token: str = Depends(security)):
    """Get user profile information"""
    try:
        decoded_token = auth.verify_id_token(token.credentials)
        user = auth.get_user(decoded_token["uid"])
        
        return {
            "uid": user.uid,
            "email": user.email,
            "display_name": user.display_name,
            "email_verified": user.email_verified,
            "created_at": user.user_metadata.creation_timestamp
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
