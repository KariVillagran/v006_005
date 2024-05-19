from fastapi import FastAPI, HTTPException
from transbank.webpay.webpay_plus.transaction import Transaction
import mysql.connector

app = FastAPI()

# Configura la conexión a la base de datos
conexion = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Kusanagi.12",
    database="ferremax"
)
cursor = conexion.cursor()


@app.post("/pagos")
async def procesar_pago(id_pedido: int):
    try:
        # Consulta el monto total del pedido en la base de datos
        cursor.execute("SELECT monto_total FROM facturas WHERE id_pedido = %s", (id_pedido,))
        row = cursor.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        
        monto_total = row[0]
        if monto_total is None:
            raise HTTPException(status_code=500, detail="Monto total del pedido no disponible")

        # Configura el SDK de Transbank
        Transaction.commerce_code = "597055555542"
        Transaction.api_key = "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C"

        # Realiza la simulación de pago
        response = Transaction.create(amount=monto_total, buy_order=str(id_pedido))

        # Aquí podrías guardar información relevante de la transacción en tu base de datos

        return {"mensaje": "Pago procesado exitosamente"}
    except mysql.connector.Error as e:
        # Maneja errores de MySQL
        return {"error": f"Error de MySQL: {str(e)}"}
    except HTTPException as e:
        # Propaga excepciones HTTP
        raise e
    except Exception as e:
        # Captura cualquier otra excepción
        return {"error": f"Error inesperado: {str(e)}"}
