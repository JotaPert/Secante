import numpy as np
from typing import Callable, Tuple, List

def _buscar_raices_aproximadas(
    funcion_objetivo: Callable[[float], float],
    limite_inferior: float,
    limite_superior: float,
    cantidad_puntos: int = 2000,
    tolerancia_cero: float = 1e-8,
) -> List[float]:
    """
    Busca raíces de una función general evaluando puntos discretos y 
    usando interpolación lineal cuando detecta un cambio de signo.
    """
    valores_x = np.linspace(limite_inferior, limite_superior, cantidad_puntos)
    valores_y = np.array([funcion_objetivo(x) for x in valores_x], dtype=float)

    raices_encontradas = []

    for i in range(len(valores_x) - 1):
        y_actual = valores_y[i]
        y_siguiente = valores_y[i + 1]

        if not np.isfinite(y_actual) or not np.isfinite(y_siguiente):
            continue

        # Si el valor es prácticamente cero, lo consideramos una raíz exacta en la malla
        if abs(y_actual) < tolerancia_cero:
            raices_encontradas.append(float(valores_x[i]))
            continue

        # Si hay un cambio de signo, la raíz cruza por cero entre estos dos puntos
        if y_actual * y_siguiente < 0:
            x_actual = valores_x[i]
            x_siguiente = valores_x[i + 1]
            # Interpolación lineal para estimar el punto exacto de cruce
            raiz_aproximada = x_actual - y_actual * (x_siguiente - x_actual) / (y_siguiente - y_actual)
            raices_encontradas.append(float(raiz_aproximada))

    # Eliminar raíces duplicadas o extremadamente cercanas (ruido de precisión)
    raices_unicas = []
    for raiz in sorted(raices_encontradas):
        if not raices_unicas or abs(raiz - raices_unicas[-1]) > 1e-5:
            raices_unicas.append(raiz)

    return raices_unicas

def calcular_intervalo_desde_raices_y_f0(
    funcion_objetivo: Callable[[float], float],
    ventana_inicial: float = 1.0,
    maximas_expansiones: int = 6,
    cantidad_puntos: int = 2000,
) -> Tuple[float, float]:
    """
    Calcula un intervalo de visualización automático buscando raíces hacia afuera.
    Asegura incluir el corte con el eje Y (x=0).
    """
    limite_actual = ventana_inicial
    raices_encontradas = []

    # Expande progresivamente la ventana de búsqueda si no encuentra raíces
    for _ in range(maximas_expansiones):
        raices_encontradas = _buscar_raices_aproximadas(
            funcion_objetivo,
            -limite_actual,
            limite_actual,
            cantidad_puntos=cantidad_puntos,
        )

        if raices_encontradas:
            break

        limite_actual *= 2.0

    if not raices_encontradas:
        # Si no hay raíces visibles tras las expansiones, centramos alrededor de x = 0
        return -limite_actual, limite_actual

    # El intervalo de interés debe contener todas las raíces y el origen
    puntos_de_interes = [0.0] + raices_encontradas
    x_minimo = min(puntos_de_interes)
    x_maximo = max(puntos_de_interes)

    amplitud_dominio = x_maximo - x_minimo
    margen_visual = max(1.0, 0.2 * amplitud_dominio)

    return x_minimo - margen_visual, x_maximo + margen_visual

def encontrar_extremos_funcion_general(funcion_objetivo: Callable[[float], float], 
    limite_inferior: float, 
    limite_superior: float, puntos_evaluacion: int = 2000) -> Tuple[float, float, float, float]:
    """
    Aproximación numérica del máximo y mínimo para cualquier función evaluando 'n' puntos en [a,b].
    """
    valores_x = np.linspace(limite_inferior, limite_superior, puntos_evaluacion)
    valores_y = np.array([funcion_objetivo(x) for x in valores_x])
    
    indice_minimo = int(np.argmin(valores_y))
    indice_maximo = int(np.argmax(valores_y))
    
    return valores_x[indice_minimo], valores_y[indice_minimo], valores_x[indice_maximo], valores_y[indice_maximo]

def construir_funcion_desde_texto(expresion_matematica: str) -> Callable[[float], float]:
    """
    Convierte un string matemático (ej. 'x**2 + sin(x)') en una función de Python evaluable.
    """
    funciones_permitidas = {
        "np": np,
        "sin": np.sin,
        "cos": np.cos,
        "tan": np.tan,
        "exp": np.exp,
        "log": np.log,
        "sqrt": np.sqrt,
        "abs": np.abs,
        "pi": np.pi,
        "e": np.e,
    }

    def funcion_evaluada(x: float) -> float:
        entorno_evaluacion = dict(funciones_permitidas)
        entorno_evaluacion["x"] = x
        # Nota de seguridad: 'eval' es peligroso con inputs no confiables, 
        # pero restringimos __builtins__ para mitigar riesgos básicos.
        return float(eval(expresion_matematica, {"__builtins__": {}}, entorno_evaluacion))

    return funcion_evaluada