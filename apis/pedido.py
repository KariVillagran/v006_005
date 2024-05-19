from fastapi import APIRouter, HTTPException, FastAPI, Depends
from pydantic import BaseModel, validator
import mysql.connector
from typing import List

app = FastAPI()

# Crear un router para las operaciones relacionadas con los pedidos
router = APIRouter()

# Configuración de la conexión a la base de datos
config = {
    'user': 'root',
    'password': 'Kusanagi.12',
    'host': '127.0.0.1',
    'database': 'ferremax',
    'port': '3306',
}

# Modelo Pydantic para la creación de productos dentro del pedido
class ProductoPedido(BaseModel):
    id_producto: int
    cantidad: int

# Modelo Pydantic para la creación de pedidos
class PedidoCreate(BaseModel):
    id_usuario: int
    fecha_pedido: str
    estado: str
    productos: List[ProductoPedido]

    @validator('productos')
    def productos_non_empty(cls, v):
        if not v:
            raise ValueError('Se requiere al menos un producto en el pedido')
        return v

# Función para establecer una nueva conexión a la base de datos
def get_connection():
    return mysql.connector.connect(**config)

# Función para obtener la información de un producto por su ID
def get_producto_info(producto_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    query = "SELECT id, nombre, precio, stock FROM productos WHERE id = %s"
    cursor.execute(query, (producto_id,))
    producto_data = cursor.fetchone()

    cursor.close()
    connection.close()

    return producto_data

# Ruta para crear un nuevo pedido
@router.post("/pedido/")
async def create_pedido(pedido: PedidoCreate):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Insertar el nuevo pedido en la base de datos
        query = "INSERT INTO pedidos (id_usuario, fecha_pedido, estado) VALUES (%s, %s, %s)"
        values = (pedido.id_usuario, pedido.fecha_pedido, pedido.estado)
        cursor.execute(query, values)
        connection.commit()

        # Obtener el ID del nuevo pedido insertado
        nuevo_pedido_id = cursor.lastrowid

        # Insertar los productos asociados al pedido en la tabla detallespedido
        for producto in pedido.productos:
            producto_info = get_producto_info(producto.id_producto)
            if producto_info:
                producto_id, nombre, precio, stock = producto_info
                if producto.cantidad <= stock:
                    query = "INSERT INTO detallespedido (id_pedido, id_producto, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)"
                    values = (nuevo_pedido_id, producto_id, producto.cantidad, precio)
                    cursor.execute(query, values)
                    connection.commit()
                else:
                    raise HTTPException(status_code=400, detail=f"No hay suficiente stock para el producto {nombre}")
            else:
                raise HTTPException(status_code=404, detail=f"No se encontró información para el producto con ID {producto.id_producto}")

    finally:
        cursor.close()
        connection.close()

    return {"message": "Pedido creado exitosamente", "pedido_id": nuevo_pedido_id}

# Agregar el router a la aplicación principal
app.include_router(router)
