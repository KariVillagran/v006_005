from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

# Definimos el modelo de Producto
class Producto(Base):
    __tablename__ = 'producto'

    IdProducto = Column(Integer, primary_key=True)
    Nombre = Column(String(100), nullable=False)
    Descripcion = Column(String(255))
    ImagenURL = Column(String(255))
    Cantidad = Column(Integer, default=0)

# Configuración de la conexión a la base de datos
DATABASE_URL = "mysql+mysqlconnector://root:Kusanagi.12@localhost/ferremax"
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Creamos una instancia de FastAPI
app = FastAPI()

# Modelo Pydantic para la creación de productos
class ProductoCreate(BaseModel):
    Nombre: str
    Descripcion: str
    ImagenURL: str
    Cantidad: int = 0

# Ruta para crear un nuevo producto
@app.post('/producto', response_model=dict)
async def crear_producto(producto: ProductoCreate):
    async with async_session() as session:
        nuevo_producto = Producto(**producto.dict())
        session.add(nuevo_producto)
        await session.commit()
        return {'mensaje': 'Producto creado correctamente'}

# Ruta para sumar la cantidad de un producto
@app.put('/producto/sumar/{IdProducto}', response_model=dict)
async def sumar_producto(IdProducto: int, cantidad: int = 1):
    async with async_session() as session:
        producto = await session.get(Producto, IdProducto)
        if producto:
            producto.Cantidad += cantidad
            await session.commit()
            return {'mensaje': f'Se han sumado {cantidad} unidades al producto {producto.Nombre}'}
        else:
            raise HTTPException(status_code=404, detail='Producto no encontrado')

# Ruta para rebajar la cantidad de un producto
@app.put('/producto/rebajar/{IdProducto}', response_model=dict)
async def rebajar_producto(IdProducto: int, cantidad: int = 1):
    async with async_session() as session:
        producto = await session.get(Producto, IdProducto)
        if producto:
            if producto.Cantidad >= cantidad:
                producto.Cantidad -= cantidad
                await session.commit()
                return {'mensaje': f'Se han rebajado {cantidad} unidades del producto {producto.Nombre}'}
            else:
                raise HTTPException(status_code=400, detail='No hay suficientes unidades disponibles para rebajar')
        else:
            raise HTTPException(status_code=404, detail='Producto no encontrado')
