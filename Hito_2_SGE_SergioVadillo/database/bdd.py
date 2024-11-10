import mysql.connector
from mysql.connector import Error

def conectar_bd():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Sergio1993*",
            database="ENCUESTAS"
        )
        return conexion
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None
