import mysql.connector

# Configuración de la conexión
config = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',  # Cambia esto si tu base de datos está en otro host
    'database': 'ferremax',  # Nombre de tu base de datos
}

# Conexión a la base de datos
conn = mysql.connector.connect(**config)

# Crear un cursor
cursor = conn.cursor()

# Ejemplo de consulta
query = "SELECT * FROM usuarios"
cursor.execute(query)

# Obtener resultados
resultados = cursor.fetchall()

# Imprimir resultados
for fila in resultados:
    print(fila)

# Cerrar la conexión
conn.close()
