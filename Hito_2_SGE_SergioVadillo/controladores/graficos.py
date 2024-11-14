import matplotlib.pyplot as plt

def graficar_datos(datos, campo):
    valores = [getattr(encuesta, campo) for encuesta in datos]
    plt.hist(valores, bins=10, label=f"Distribución de {campo}")
    plt.xlabel(campo)
    plt.ylabel("Frecuencia")
    plt.title(f"Distribución de {campo}")
    plt.legend(loc="upper right")  # Agregar la leyenda en la esquina superior derecha
    plt.show()
