

from pydantic import BaseModel

class UserExtend(BaseModel):
    nombre: str
    apellido: str
    rol: str
