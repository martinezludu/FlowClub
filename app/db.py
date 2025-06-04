from app.config import SUPABASE_URL, SUPABASE_KEY,SUPABASE_SERVICE_ROLE_KEY
import httpx
from supabase import create_client

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

async def get_users():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SUPABASE_URL}/rest/v1/users", headers=headers)
        return response.json()
    


supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
