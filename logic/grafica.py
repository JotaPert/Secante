import numpy as np
import matplotlib.pyplot as plt
from typing import Callable

def graficar_funcion_general(
    funcion_objetivo: Callable[[float], float],
    expresion_matematica: str,
    limite_inferior: float,
    limite_superior: float,
    x_minimo: float,
    y_minimo: float,
    x_maximo: float,
    y_maximo: float
) -> None:
    """
    Se encarga exclusivamente de renderizar el gráfico de la función y sus extremos.
    """
    resolucion_x = np.linspace(limite_inferior, limite_superior, 1500)
    valores_y = np.array([funcion_objetivo(x) for x in resolucion_x])

    plt.figure(figsize=(9, 5))
    plt.plot(resolucion_x, valores_y, label="f(x)")
    
    # Resaltamos los puntos extremos
    plt.scatter([x_minimo, x_maximo], [y_minimo, y_maximo], 
                s=70, color="red", label="Extremos aproximados", zorder=3)
    
    # Línea del eje X
    plt.axhline(0.0, color="black", linestyle="--", linewidth=1, alpha=0.5)
    
    plt.title(f"Análisis de: f(x) = {expresion_matematica}")
    plt.xlabel("Eje X")
    plt.ylabel("f(x)")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.show()