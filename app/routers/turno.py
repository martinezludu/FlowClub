from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_turnos():
    return [{"id": 1, "espacio": "Cancha", "horario": "18:00"}]

@router.post("/")
async def reservar_turno(turno: dict):
    return {"msg": "Turno reservado", "turno": turno}