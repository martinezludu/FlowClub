from fastapi import FastAPI
from app.routers import user, turno, auth
import uvicorn

app = FastAPI(title="ClubFlow API")

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(turno.router, prefix="/turnos", tags=["turnos"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)