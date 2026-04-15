import numpy as np
import matplotlib.pyplot as plt
from typing import Callable, Optional

def graficar_funcion_general(
    funcion_objetivo: Callable[[float], float],
    expresion_matematica: str,
    limite_inferior: float,
    limite_superior: float,
    x_minimo: float,
    y_minimo: float,
    x_maximo: float,
    y_maximo: float
    ,
    mostrar: bool = True,
) -> Optional[plt.Figure]:
    """
    Se encarga exclusivamente de renderizar el gráfico de la función y sus extremos.
    """
    resolucion_x = np.linspace(limite_inferior, limite_superior, 1500)
    valores_y = np.array([funcion_objetivo(x) for x in resolucion_x])

    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.plot(resolucion_x, valores_y, label="f(x)", color="#2563eb", linewidth=2)
    
    # Resaltamos los puntos extremos
    ax.scatter([x_minimo, x_maximo], [y_minimo, y_maximo],
               s=75, color="#ef4444", label="Extremos aproximados", zorder=3)
    
    # Línea del eje X
    ax.axhline(0.0, color="#111827", linestyle="--", linewidth=1, alpha=0.35)
    
    ax.set_title(f"Análisis de: f(x) = {expresion_matematica}")
    ax.set_xlabel("Eje X")
    ax.set_ylabel("f(x)")
    ax.grid(alpha=0.25)
    ax.legend()

    if mostrar:
        plt.show()
        return None

    return fig