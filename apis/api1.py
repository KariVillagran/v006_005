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

# Operación POST para iniciar sesión
@app.post("/login/")
def login(credentials: dict):
    email = credentials.get("email")
    password = credentials.get("password")
    if not email or not password:
        raise HTTPException(status_code=400, detail="Correo electrónico y contraseña son necesarios")
    
    try:
        # Establecer conexión
        conn = get_connection()
        
        # Crear cursor
        cursor = conn.cursor()
        
        # Buscar usuario por correo electrónico
        query = "SELECT * FROM usuarios WHERE email = %s"
        cursor.execute(query, (email,))
        usuario = cursor.fetchone()
        
        if usuario:
            # Verificar la contraseña
            if password == usuario[3]:  # La contraseña está en el índice 3
                return {"mensaje": "Inicio de sesión exitoso"}
            else:
                raise HTTPException(status_code=401, detail="Credenciales inválidas")
        else:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
    except mysql.connector.Error as err:
        return {"error": f"Error al conectar a la base de datos: {err}"}
    finally:
        # Intentar cerrar la conexión si está definida
        try:
            conn.close()
        except NameError:
            pass
        # Intentar cerrar el cursor si está definido
        try:
            cursor.close()
        except NameError:
            pass

# Operación GET para obtener todos los usuarios
@app.get("/usuarios/")
def obtener_usuarios():
    try:
        # Establecer conexión
        conn = get_connection()
        
        # Crear cursor
        cursor = conn.cursor()
        
        # Ejecutar consulta
        query = "SELECT * FROM usuarios"
        cursor.execute(query)
        
        # Obtener resultados
        usuarios = cursor.fetchall()
        
        # Cerrar cursor y conexión
        cursor.close()
        conn.close()
        
        return {"usuarios": usuarios}
    except mysql.connector.Error as err:
        return {"error": f"Error al conectar a la base de datos: {err}"}

# Operación GET para obtener un usuario por su ID
@app.get("/usuarios/{usuarios_id}")
def obtener_usuario(usuarios_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM usuarios WHERE id = %s"
    cursor.execute(query, (usuarios_id,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    if usuario:
        return usuario
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

# Operación POST para agregar un nuevo usuario
@app.post("/usuarios/")
def agregar_usuario(nombre: str, email: str):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO usuarios (nombre, email) VALUES (%s, %s)"
    cursor.execute(query, (nombre, email))
    conn.commit()
    cursor.close()
    conn.close()
    return {"mensaje": "Usuario agregado correctamente"}

# Operación PUT para actualizar un usuario
@app.put("/usuarios/{usuario_id}")
def actualizar_usuario(usuario_id: int, nombre: str, email: str):
    conn = get_connection()
    cursor = conn.cursor()
    query = "UPDATE usuarios SET nombre = %s, email = %s WHERE id = %s"
    cursor.execute(query, (nombre, email, usuario_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"mensaje": "Usuario actualizado correctamente"}

# Operación DELETE para eliminar un usuario
@app.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    query = "DELETE FROM usuarios WHERE id = %s"
    cursor.execute(query, (usuario_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"mensaje": "Usuario eliminado correctamente"}
