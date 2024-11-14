# Hito2_SistemasdeGestionEmpresarial

## Descripción
Este proyecto se centra en un sistema para gestionar encuestas sobre el consumo de alcohol y su conexión con problemas de salud. La aplicación facilita realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) en los datos guardados en una base de datos MySQL y permite visualizar los resultados a través de gráficos generados con matplotlib.


## Introducción  
El objetivo de este estudio es examinar los patrones de consumo de alcohol y su efecto en la salud de los encuestados. Mediante una interfaz gráfica intuitiva, los usuarios pueden ingresar y analizar datos para detectar tendencias y correlaciones. Este sistema busca simplificar la gestión de datos y optimizar la toma de decisiones en el área de la salud.
instrucciones claras sobre cómo configurar y ejecutar el proyecto, incluyendo:

## Configuración e Instalación
Para ejecutar este proyecto, se requiere la instalación de python 3.10+

Para que el programa funcione correctamente habría que ejecutar en comandos estos pip installs que garantizan que las bibliotecas necesarias estén disponibles para ejecutar las funcionalidades del proyecto (base de datos, gráficos, y exportación).

-pip install mysql-connector-python
-Alomejor también pip install mysql.connector
-pip install pandas
-pip install matlotlib
-pandas matplotlib

## Configuración de MySQL:

Crear la base de datos ENCUESTAS usando el sql del proyecto.

Si da error de caching_sha2_password al ejectar el main.py significa que te ha puesto un codificador de contraseña automáticamente y lo que necesitas esla contraseña de origen, entonces hay que usar este alter table para que se quede con su contraseña sin codificar:

Este ALTER TABLE corrige problemas en la estructura de la base de datos, asegurando que se puedan insertar datos sin conflictos.

ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'tu_password';
FLUSH PRIVILEGES;

También habría que añadir esto en la parte de código de conexión a la base de datos para que funcione:
auth_plugin='mysql_native_password'

