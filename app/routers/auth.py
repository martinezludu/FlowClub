from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx
from app.config import SUPABASE_URL,SUPABASE_KEY

router = APIRouter()
security = HTTPBearer()

@router.get("/me")
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    headers = {
        "Authorization": f"Bearer {token}",
        "apikey": SUPABASE_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SUPABASE_URL}/auth/v1/user",
            headers=headers
        )

    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    return response.json()