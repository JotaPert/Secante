import numpy as np
import matplotlib.pyplot as plt
from typing import Callable, Optional
import re


def _detectar_intersecciones_eje_x(
    valores_x: np.ndarray,
    valores_y: np.ndarray,
    tolerancia_cero: float = 1e-4,
) -> list[float]:
    """
    Detecta raices aproximadas usando malla discreta y cambios de signo.
    """
    raices_encontradas: list[float] = []

    for i in range(len(valores_x) - 1):
        y_actual = float(valores_y[i])
        y_siguiente = float(valores_y[i + 1])

        if not np.isfinite(y_actual) or not np.isfinite(y_siguiente):
            continue

        if abs(y_actual) < tolerancia_cero:
            raices_encontradas.append(float(valores_x[i]))
            continue

        if abs(y_siguiente) < tolerancia_cero:
            raices_encontradas.append(float(valores_x[i + 1]))
            continue

        if y_actual * y_siguiente < 0:
            x_actual = float(valores_x[i])
            x_siguiente = float(valores_x[i + 1])
            raiz_aproximada = x_actual - y_actual * (x_siguiente - x_actual) / (y_siguiente - y_actual)
            raices_encontradas.append(float(raiz_aproximada))

    # Captura raíces tangentes (multiplicidad par) buscando mínimos locales de |f(x)| cercanos a cero.
    for i in range(1, len(valores_x) - 1):
        y_anterior = abs(float(valores_y[i - 1]))
        y_actual_abs = abs(float(valores_y[i]))
        y_siguiente = abs(float(valores_y[i + 1]))

        if (
            np.isfinite(y_anterior)
            and np.isfinite(y_actual_abs)
            and np.isfinite(y_siguiente)
            and y_actual_abs < tolerancia_cero
            and y_actual_abs <= y_anterior
            and y_actual_abs <= y_siguiente
        ):
            raices_encontradas.append(float(valores_x[i]))

    raices_unicas: list[float] = []
    for raiz in sorted(raices_encontradas):
        if not raices_unicas or abs(raiz - raices_unicas[-1]) > 1e-5:
            raices_unicas.append(raiz)

    return raices_unicas


def _buscar_raices_reales_en_ventana_dinamica(
    funcion_objetivo: Callable[[float], float],
    limite_inferior: float,
    limite_superior: float,
    puntos_por_malla: int = 5000,
    maximas_expansiones: int = 6,
) -> list[float]:
    """
    Busca raíces reales expandiendo la ventana para reducir el riesgo de perder intersecciones.
    """
    raices_acumuladas: list[float] = []
    x_inf = float(limite_inferior)
    x_sup = float(limite_superior)
    cantidad_anterior = -1

    for _ in range(maximas_expansiones):
        valores_x = np.linspace(x_inf, x_sup, puntos_por_malla)
        valores_y = np.array([funcion_objetivo(x) for x in valores_x], dtype=float)
        nuevas_raices = _detectar_intersecciones_eje_x(valores_x, valores_y)

        for raiz in nuevas_raices:
            if not raices_acumuladas or all(abs(raiz - r) > 1e-5 for r in raices_acumuladas):
                raices_acumuladas.append(raiz)

        raices_acumuladas.sort()

        # Si la cantidad de raíces ya no cambia y tenemos al menos una, detenemos expansión.
        if raices_acumuladas and len(raices_acumuladas) == cantidad_anterior:
            break

        cantidad_anterior = len(raices_acumuladas)

        ancho_actual = x_sup - x_inf
        margen = max(1.0, 0.7 * ancho_actual)
        x_inf -= margen
        x_sup += margen

    return raices_acumuladas


def _formatear_expresion_para_mathtext(expresion: str) -> str:
    """
    Convierte una expresion de entrada a una forma legible para mostrar en titulo.
    Ejemplo: x**3 - 2*x**2 - x + 2 -> x^{3} - 2x^{2} - x + 2
    """
    texto = expresion.strip().replace("**", "^")
    texto = texto.replace("*", "")
    texto = re.sub(r"\^(\-?\d+)", r"^{\1}", texto)
    return texto

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
    Renderiza la funcion priorizando las intersecciones con el eje X (raices).
    """
    raices_aproximadas = _buscar_raices_reales_en_ventana_dinamica(
        funcion_objetivo,
        limite_inferior,
        limite_superior,
    )

    # Definimos primero el rango a visualizar para que la curva se muestree completa.
    x_plot_inf = limite_inferior
    x_plot_sup = limite_superior

    if raices_aproximadas:
        x_min_raices = min(raices_aproximadas)
        x_max_raices = max(raices_aproximadas)
        ancho_raices = x_max_raices - x_min_raices
        margen_x = max(0.8, 0.9 * ancho_raices)
        x_plot_inf = x_min_raices - margen_x
        x_plot_sup = x_max_raices + margen_x

    resolucion_x = np.linspace(x_plot_inf, x_plot_sup, 2000)
    valores_y = np.array([funcion_objetivo(x) for x in resolucion_x])

    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.plot(resolucion_x, valores_y, label="f(x)", color="#2563eb", linewidth=2)
    
    # Línea del eje X
    ax.axhline(0.0, color="#111827", linestyle="--", linewidth=1, alpha=0.35)

    # Intersecciones con eje X (raices)
    if raices_aproximadas:
        ax.scatter(
            raices_aproximadas,
            [0.0] * len(raices_aproximadas),
            s=92,
            color="#16a34a",
            edgecolor="#14532d",
            linewidth=1.1,
            label="Raices aproximadas",
            zorder=5,
        )

        for raiz in raices_aproximadas:
            ax.annotate(
                f"x={raiz:.3f}",
                xy=(raiz, 0.0),
                xytext=(0, 10),
                textcoords="offset points",
                ha="center",
                fontsize=9,
                color="#14532d",
            )

        # Centramos la vista horizontalmente en las raices para darles prioridad visual.
        ax.set_xlim(x_plot_inf, x_plot_sup)

        mascara_rango = (resolucion_x >= x_plot_inf) & (resolucion_x <= x_plot_sup)
        y_rango = valores_y[mascara_rango]
        max_abs_y = float(np.max(np.abs(y_rango))) if y_rango.size else 1.0
        max_abs_y = max(1.0, max_abs_y)
        ax.set_ylim(-1.2 * max_abs_y, 1.2 * max_abs_y)

        texto_raices = ", ".join(f"x={raiz:.4f}" for raiz in raices_aproximadas)
        fig.text(
            0.5,
            0.03,
            f"Raices reales aproximadas: {texto_raices}",
            ha="center",
            va="center",
            fontsize=10,
            color="#111827",
        )
    else:
        fig.text(
            0.5,
            0.03,
            "No se detectaron raices reales en el intervalo analizado.",
            ha="center",
            va="center",
            fontsize=10,
            color="#374151",
        )
    
    expresion_titulo = _formatear_expresion_para_mathtext(expresion_matematica)
    ax.set_title(rf"Intersecciones con eje X: $f(x) = {expresion_titulo}$")
    ax.set_xlabel("Eje X")
    ax.set_ylabel("f(x)")
    ax.grid(alpha=0.25)
    ax.legend(loc="best")
    fig.tight_layout(rect=(0, 0.06, 1, 1))

    if mostrar:
        plt.show()
        return None

    return fig