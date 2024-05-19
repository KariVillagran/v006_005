from fastapi import APIRouter, HTTPException, FastAPI
import mysql.connector

# Crear un router para las operaciones relacionadas con las sucursales
router = APIRouter()

# Configuración de la conexión a la base de datos
config = {
    'user': 'root',
    'password': 'Kusanagi.12',
    'host': '127.0.0.1',
    'database': 'ferremax',
    'port': '3306',
}

# Función para establecer una nueva conexión a la base de datos
def get_connection():
    return mysql.connector.connect(**config)

# Ruta para asociar una sucursal a un pedido existente
@router.put("/pedido/{pedido_id}/sucursal/{sucursal_id}")
async def asociar_sucursal(pedido_id: int, sucursal_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Verificar si el pedido existe
        cursor.execute("SELECT * FROM pedidos WHERE id = %s", (pedido_id,))
        pedido = cursor.fetchone()
        if pedido is None:
            raise HTTPException(status_code=404, detail="El pedido especificado no existe")

        # Verificar si la sucursal existe
        cursor.execute("SELECT * FROM sucursales WHERE id = %s", (sucursal_id,))
        sucursal = cursor.fetchone()
        if sucursal is None:
            raise HTTPException(status_code=404, detail="La sucursal especificada no existe")

        # Asociar la sucursal al pedido
        cursor.execute("UPDATE pedidos SET id_sucursal = %s WHERE id = %s", (sucursal_id, pedido_id))
        connection.commit()

        return {"message": "Sucursal asociada al pedido correctamente"}

    finally:
        cursor.close()
        connection.close()



# Agregar el router a la aplicación principal
# En este caso, debes tener una instancia de FastAPI
app = FastAPI()
app.include_router(router)
