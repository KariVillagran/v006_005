from fastapi import FastAPI, HTTPException, Body
from sqlalchemy import create_engine, Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import List

# Crear una instancia de FastAPI
app = FastAPI()

# Configurar la conexión a la base de datos MariaDB
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:Kusanagi.12@127.0.0.1/ferremax"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Definir las clases de modelos SQLAlchemy
class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), index=True)
    precio = Column(Numeric(10, 2))
    stock = Column(Integer)

class DetallePedido(Base):
    __tablename__ = "detallespedido"

    id = Column(Integer, primary_key=True, index=True)
    id_pedido = Column(Integer, ForeignKey("pedidos.id"))
    id_producto = Column(Integer, ForeignKey("productos.id"))
    cantidad = Column(Integer)
    precio_unitario = Column(Numeric(10, 2))

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer)
    fecha_pedido = Column(String)
    estado = Column(String)
    detalles = relationship("DetallePedido", back_populates="pedido")

    def calcular_total(self):
        total = 0
        for detalle in self.detalles:
            total += detalle.cantidad * detalle.precio_unitario
        return total

class DetallePedidoIn(BaseModel):
    id_producto: int
    cantidad: int

class Factura(BaseModel):
    id_pedido: int
    fecha_emision: str
    monto_total: float
    iva: float

# Crear las tablas en la base de datos (solo para propósitos de demostración, en producción esto se haría con un script de migración)
Base.metadata.create_all(bind=engine)

# Endpoint para crear un pedido con sus detalles
@app.post("/pedidos/", response_model=Pedido)
def create_pedido(detalles: List[DetallePedidoIn] = Body(...)):
    db = SessionLocal()
    try:
        # Crear el pedido
        pedido = Pedido(id_usuario=1, fecha_pedido="2024-05-13", estado="pendiente")
        db.add(pedido)
        db.commit()
        db.refresh(pedido)

        # Agregar los detalles del pedido
        for detalle in detalles:
            producto = db.query(Producto).filter(Producto.id == detalle.id_producto).first()
            if producto is None:
                raise HTTPException(status_code=404, detail="Producto no encontrado")
            detalle_pedido = DetallePedido(
                id_pedido=pedido.id,
                id_producto=detalle.id_producto,
                cantidad=detalle.cantidad,
                precio_unitario=producto.precio
            )
            db.add(detalle_pedido)
        db.commit()
        db.refresh(pedido)

        return pedido
    finally:
        db.close()

# Endpoint para generar la factura de un pedido
@app.post("/facturas/", response_model=Factura)
def create_factura(pedido_id: int):
    db = SessionLocal()
    try:
        pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
        if pedido is None:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        
        total = pedido.calcular_total()
        iva = total * 0.19  # Suponiendo un IVA del 19%

        factura = Factura(id_pedido=pedido_id, fecha_emision="2024-05-13", monto_total=total, iva=iva)
        return factura
    finally:
        db.close()

# Si deseas probarlo, ejecuta uvicorn en la terminal:
# uvicorn main:app --reload
from fastapi import FastAPI, HTTPException, Body
from sqlalchemy import create_engine, Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import List

# Crear una instancia de FastAPI
app = FastAPI()

# Configurar la conexión a la base de datos MariaDB
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:Kusanagi.12@localhost/ferremas_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Definir las clases de modelos SQLAlchemy
class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), index=True)
    precio = Column(Numeric(10, 2))
    stock = Column(Integer)

class DetallePedido(Base):
    __tablename__ = "detallespedido"

    id = Column(Integer, primary_key=True, index=True)
    id_pedido = Column(Integer, ForeignKey("pedidos.id"))
    id_producto = Column(Integer, ForeignKey("productos.id"))
    cantidad = Column(Integer)
    precio_unitario = Column(Numeric(10, 2))

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer)
    fecha_pedido = Column(String)
    estado = Column(String)
    detalles = relationship("DetallePedido", back_populates="pedido")

    def calcular_total(self):
        total = 0
        for detalle in self.detalles:
            total += detalle.cantidad * detalle.precio_unitario
        return total

class DetallePedidoIn(BaseModel):
    id_producto: int
    cantidad: int

class Factura(BaseModel):
    id_pedido: int
    fecha_emision: str
    monto_total: float
    iva: float

# Crear las tablas en la base de datos (solo para propósitos de demostración, en producción esto se haría con un script de migración)
Base.metadata.create_all(bind=engine)

# Endpoint para crear un pedido con sus detalles
@app.post("/pedidos/", response_model=Pedido)
def create_pedido(detalles: List[DetallePedidoIn] = Body(...)):
    db = SessionLocal()
    try:
        # Crear el pedido
        pedido = Pedido(id_usuario=1, fecha_pedido="2024-05-13", estado="pendiente")
        db.add(pedido)
        db.commit()
        db.refresh(pedido)

        # Agregar los detalles del pedido
        for detalle in detalles:
            producto = db.query(Producto).filter(Producto.id == detalle.id_producto).first()
            if producto is None:
                raise HTTPException(status_code=404, detail="Producto no encontrado")
            detalle_pedido = DetallePedido(
                id_pedido=pedido.id,
                id_producto=detalle.id_producto,
                cantidad=detalle.cantidad,
                precio_unitario=producto.precio
            )
            db.add(detalle_pedido)
        db.commit()
        db.refresh(pedido)

        return pedido
    finally:
        db.close()

# Endpoint para generar la factura de un pedido
@app.post("/facturas/", response_model=Factura)
def create_factura(pedido_id: int):
    db = SessionLocal()
    try:
        pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
        if pedido is None:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        
        total = pedido.calcular_total()
        iva = total * 0.19  # Suponiendo un IVA del 19%

        factura = Factura(id_pedido=pedido_id, fecha_emision="2024-05-13", monto_total=total, iva=iva)
        return factura
    finally:
        db.close()

# Si deseas probarlo, ejecuta uvicorn en la terminal:
# uvicorn main:app --reload
