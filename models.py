from pydantic import BaseModel

class Usuario(BaseModel):
    id: int
    nombre: str
    email: str
    contrasena: str
    rol: str
