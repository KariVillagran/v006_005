from fastapi import FastAPI, HTTPException
import mysql.connector

app = FastAPI()

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

@app.get('/productos/')
async def obtener_productos():
    try:
        # Establecer conexión con la base de datos
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        # Obtener todos los productos de la base de datos
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()

        # Cerrar conexión con la base de datos
        cursor.close()
        connection.close()

        # Retornar los productos obtenidos de manera más ordenada
        productos_ordenados = []
        for idx, producto in enumerate(productos, start=1):
            producto_ordenado = {
                "id_producto": idx,
                "nombre": producto['nombre'],
                "precio": producto['precio'],
                "stock": producto['stock']
            }
            productos_ordenados.append(producto_ordenado)

        return {"productos": productos_ordenados}
    except mysql.connector.Error as error:
        # En caso de error, retornar un mensaje de error
        raise HTTPException(status_code=500, detail=f"Error al obtener productos: {str(error)}")
