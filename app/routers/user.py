from fastapi import APIRouter
from app.db import get_users

router = APIRouter()

@router.get("/")
async def list_users():
    return await get_users()

@router.post("/")
async def create_user(user: dict):
    return {"msg": "Usuario creado", "user": user}