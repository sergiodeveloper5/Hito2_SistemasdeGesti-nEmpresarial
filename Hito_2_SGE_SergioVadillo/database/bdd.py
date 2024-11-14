import mysql.connector  # Librería para conectarse a bases de datos MySQL
from mysql.connector import Error  # Manejo de excepciones específicas de MySQL

def conectar_bd():
    """
    Establece la conexión con la base de datos MySQL.

    Proporciona la configuración necesaria para conectarse al servidor de MySQL, 
    incluyendo el host, usuario, contraseña y nombre de la base de datos.
    Maneja errores si la conexión falla.

    Returns:
        mysql.connector.connection: Objeto de conexión a la base de datos si es exitoso.
        None: Si ocurre un error al intentar conectarse.
    """
    try:
        # Parámetros de conexión a la base de datos
        conexion = mysql.connector.connect(
            host="localhost",  # Dirección del servidor MySQL (local en este caso)
            user="root",       # Nombre de usuario para la conexión
            password="campusfp",  # Contraseña asociada al usuario
            database="ENCUESTAS",  # Nombre de la base de datos a la que se conecta
            auth_plugin='mysql_native_password'  # Método de autenticación
        )
        return conexion  # Devuelve la conexión si es exitosa
    except Error as e:
        # Captura errores específicos de MySQL y los muestra en consola
        print(f"Error al conectar a MySQL: {e}")
        return None  # Devuelve None si no puede conectarse
