from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models
from sqlalchemy.orm import Session
from apis import api1, datos_entrega, pago, productos, sucursal, pedido
from apis.sucursal import router as sucursal_router

app = FastAPI()

# Agregar el router de sucursal a la aplicación principal
app.include_router(sucursal_router)

SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root/Kusanagi.12/ferremax"

# Configuración de la conexión a la base de datos
config = {
    'user': 'root',
    'password': 'Kusanagi.12',
    'host': '127.0.0.1',
    'database': 'ferremax',
}

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para obtener una sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Montar las APIs en la aplicación FastAPI
app.mount("/api1", api1.app)
app.mount("/api2", productos.app)
app.mount("/api3", pedido.app)
app.mount("/api4", pago.app)
app.mount("/api5", datos_entrega.app)
app.mount("/api6", sucursal.app)

# Endpoint raíz para método GET
@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a mi API!"}
    
# Endpoint raíz para método POST
@app.post("/")
def create_item(item: dict):
    return item

# Función para obtener un usuario por su ID desde la base de datos
def get_user(db: Session, usuario_id: int):
    return db.query(models.User).filter(models.User.id == usuario_id).first()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
