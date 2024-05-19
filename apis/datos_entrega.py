from fastapi import APIRouter, HTTPException, FastAPI
import mysql.connector

# Crear un router para las operaciones relacionadas con los datos de entrega
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

# Ruta para agregar los datos de entrega a un pedido existente
@router.put("/pedido/{pedido_id}/datos_entrega/")
async def agregar_datos_entrega(pedido_id: int, datos_entrega: dict):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Verificar si el pedido existe
        cursor.execute("SELECT * FROM pedidos WHERE id = %s", (pedido_id,))
        pedido = cursor.fetchone()
        if pedido is None:
            raise HTTPException(status_code=404, detail="El pedido especificado no existe")

        # Agregar los datos de entrega al pedido
        cursor.execute("""
            UPDATE pedidos 
            SET direccion_entrega = %s, fecha_entrega = %s 
            WHERE id = %s
        """, (datos_entrega["direccion"], datos_entrega["fecha"], pedido_id))
        connection.commit()

        # Agregar los datos de entrega a la tabla direcciones
        cursor.execute("""
            INSERT INTO direcciones (direccion, comuna, region, pais, codigo_postal) 
            VALUES (%s, %s, %s, %s, %s)
        """, (datos_entrega["direccion"], datos_entrega["comuna"], datos_entrega["region"], datos_entrega["pais"], datos_entrega["codigo_postal"]))
        connection.commit()

        return {"message": "Datos de entrega agregados al pedido correctamente"}

    finally:
        cursor.close()
        connection.close()

# Agregar el router a la aplicación principal
app = FastAPI()
app.include_router(router)
