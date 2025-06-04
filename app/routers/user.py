from fastapi import APIRouter,Depends, HTTPException
from app.db import get_users
from app.routers.auth import get_current_user
from app.db import supabase
from app.schemas import UserExtend
from app.config import SUPABASE_URL, SUPABASE_KEY






router = APIRouter()

# Endpoint para obtener el usuario logueado
@router.get("/user/me",summary="Obtener usuario logueado",description="Devuelve los datos del usuario logueado. Requiere autenticación.")
def get_logged_user(current_user: dict = Depends(get_current_user)):
    return current_user
# Traemos los datos extendidos del usuario
@router.get("/user/me/extended",summary="Obtener datos extendidos del usuario",description="Devuelve los datos extendidos del usuario logueado. Requiere autenticación.")
def get_extended_user(current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]

    res = supabase.table("users").select("*").eq("id", user_id).execute()
    
    if not res.data:
        raise HTTPException(status_code=404, detail="Datos extendidos no encontrados")

    return res.data[0]


# Creado para extender los datos del usuario
@router.post("/user/extend",summary="Extender datos del usuario",description="Extiende los datos del usuario con nombre, apellido y rol. Debe ser llamado una sola vez por usuario.")
def extend_user(
    exteded_user: UserExtend,
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user["id"]
    nombre = payload.get("nombre")
    apellido = payload.get("apellido")
    rol = payload.get("rol")

    if not all([nombre, apellido, rol]):
        raise HTTPException(status_code=400, detail="Faltan campos obligatorios")

    # Verificamos si ya existe
    res = supabase.table("users").select("id").eq("id", current_user["id"]).execute()
    if res.data:
        raise HTTPException(status_code=409, detail="Ya existe una fila extendida para este usuario")

    # Insertamos si no existe
    response = supabase.table("users").insert({
        "id": current_user["id"],
        "nombre": nombre,
        "apellido": apellido,
        "rol": rol
    }).execute()

    # Verificar si hubo un error en la inserción
    if response.get("error"):
        raise HTTPException(status_code=500, detail=response["error"]["message"])

    return {"message": "Usuario extendido registrado con éxito"}


# Endpoint para actualizar los datos extendidos del usuario
@router.put("/user/me/extended",summary="Actualizar datos extendidos del usuario",description="Actualiza los datos extendidos del usuario logueado. Debe ser llamado una sola vez por usuario.")
def update_extended_user(
    extend_data: UserExtend,
    current_user: dict = Depends(get_current_user)
):
    # Verificamos si el usuario extendido ya existe
    res = supabase.table("users").select("id").eq("id", current_user["id"]).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="No se encontró el usuario extendido")

    # Actualizamos los datos
    supabase.table("users").update({
        "nombre": extend_data.nombre,
        "apellido": extend_data.apellido,
        "rol": extend_data.rol
    }).eq("id", current_user["id"]).execute()

    return {"message": "Datos actualizados correctamente"}


@router.delete("/user/me/extended",summary="Eliminar datos extendidos del usuario",description="Elimina los datos extendidos del usuario logueado.")
def delete_extended_user(current_user: dict = Depends(get_current_user)):
    supabase.table("users").delete().eq("id", current_user["id"]).execute()
    return {"message": "Datos extendidos eliminados"}

@router.delete("/user/me/full",summary="Eliminar usuario completamente",description="Elimina el usuario logueado y sus datos extendidos de la base de datos y Supabase Auth.")
def delete_user_completely(current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]

    # Borrar datos extendidos
    supabase.table("users").delete().eq("id", user_id).execute()

    # Borrar de Supabase Auth
    headers = {
        "apikey": SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}"
    }
    response = httpx.delete(
        f"{SUPABASE_URL}/auth/v1/admin/users/{user_id}",
        headers=headers
    )

    if response.status_code != 204:
        raise HTTPException(status_code=500, detail="Error al eliminar usuario de Supabase Auth")

    return {"message": "Usuario eliminado completamente"}