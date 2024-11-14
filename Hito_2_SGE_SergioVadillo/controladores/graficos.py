import matplotlib.pyplot as plt  # Librería para visualización de gráficos

def graficar_datos(datos, campo):
    """
    Genera un histograma basado en un conjunto de datos y un campo específico.

    Args:
        datos (list): Lista de objetos que representan encuestas u otros registros.
        campo (str): Nombre del atributo del objeto a graficar.

    Detalles:
        - Se extraen los valores del atributo especificado en `campo` de cada objeto en `datos`.
        - Se genera un histograma para visualizar la distribución de los valores.
        - El histograma incluye etiquetas y una leyenda.

    """
    # Extraer los valores del campo especificado de cada objeto en la lista
    valores = [getattr(encuesta, campo) for encuesta in datos]

    # Crear un histograma con los valores extraídos
    plt.hist(valores, bins=10, label=f"Distribución de {campo}")

    # Etiquetas de los ejes
    plt.xlabel(campo)  # Etiqueta para el eje X basada en el campo seleccionado
    plt.ylabel("Frecuencia")  # Etiqueta para el eje Y indicando la frecuencia

    # Título del gráfico
    plt.title(f"Distribución de {campo}")

    # Agregar una leyenda en la esquina superior derecha
    plt.legend(loc="upper right")

    # Mostrar el gráfico
    plt.show()
