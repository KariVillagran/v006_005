from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector

# Definimos la clase para la conexión a la base de datos
class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Kusanagi.12',
            database='ferremax'
        )

    def assign_role(self, user_id: int, role_id: int):
        try:
            with self.connection.cursor() as cursor:
                # Ejecutar la consulta para asignar el rol al usuario
                sql = "UPDATE usuarios SET IdRol = %s WHERE IdUsuario = %s"
                cursor.execute(sql, (role_id, user_id))
            self.connection.commit()
        except Exception as e:
            print("Error al asignar el rol:", e)
            self.connection.rollback()
            raise HTTPException(status_code=500, detail="Error interno del servidor")

    def register_delivery(self, delivery_data: dict):
        try:
            with self.connection.cursor() as cursor:
                # Insertar el registro de entrega en la tabla RegistroEntrega
                sql = "INSERT INTO RegistroEntrega (IdUsuario, IdProducto, Cantidad) VALUES (%s, %s, %s)"
                cursor.execute(sql, (delivery_data['IdUsuario'], delivery_data['IdProducto'], delivery_data['Cantidad']))
            self.connection.commit()
        except Exception as e:
            print("Error al registrar la entrega:", e)
            self.connection.rollback()
            raise HTTPException(status_code=500, detail="Error interno del servidor")

    def get_financial_report(self):
        try:
            with self.connection.cursor() as cursor:
                # Consulta para obtener el reporte financiero
                sql = """
                    SELECT 
                        c.Nombre as Cliente, 
                        p.Nombre as Producto, 
                        r.Cantidad, 
                        p.Valor * r.Cantidad as Total,
                        SUM(r.Cantidad) OVER (PARTITION BY r.IdProducto) as TotalVendido,
                        p.Stock as StockActual
                    FROM 
                        RegistroEntrega r 
                        JOIN Cliente c ON r.IdUsuario = c.IdUsuario 
                        JOIN Producto p ON r.IdProducto = p.IdProducto
                """
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        except Exception as e:
            print("Error al generar el reporte financiero:", e)
            raise HTTPException(status_code=500, detail="Error interno del servidor")

    def close(self):
        self.connection.close()

# Definimos los modelos Pydantic
class User(BaseModel):
    IdUsuario: int

class Role(BaseModel):
    IdRol: int
    Descripcion: str

class Delivery(BaseModel):
    IdUsuario: int
    IdProducto: int
    Cantidad: int

# Creamos una instancia de FastAPI
app = FastAPI()

# Creamos una instancia de la clase Database
db = Database()

# Definimos el endpoint para asignar un rol a un usuario
@app.put("/assign-role/")
async def assign_role(user: User, role: Role):
    try:
        db.assign_role(user.IdUsuario, role.IdRol)
        return {"message": f"Rol asignado correctamente al usuario {user.IdUsuario}"}
    except HTTPException as e:
        raise e
    finally:
        db.close()

# Endpoint para registrar la entrega de productos al cliente
@app.post("/register-delivery/")
async def register_delivery(delivery: Delivery):
    try:
        db.register_delivery(delivery.dict())
        return {"message": "Entrega registrada correctamente"}
    except HTTPException as e:
        raise e
    finally:
        db.close()

# Endpoint para obtener el reporte financiero
@app.get("/financial-report/")
async def financial_report():
    try:
        report = db.get_financial_report()
        return report
    except HTTPException as e:
        raise e
    finally:
        db.close()
