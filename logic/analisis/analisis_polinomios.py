import numpy as np
from numpy.polynomial import Polynomial
from typing import Sequence, Tuple

TOLERANCIA_IMAGINARIA = 1e-10

def _calcular_cota_cauchy(coeficientes_descendentes: Sequence[float]) -> float:
    """
    Calcula la Cota de Cauchy para las raíces de un polinomio.
    Garantiza que todas las raíces (reales y complejas) cumplen |x| <= R.
    
    Args:
        coeficientes_descendentes: Lista de coeficientes ordenados de mayor a menor grado [a_n, ..., a_0].
    Returns:
        float: El radio R de la cota de Cauchy.
    """
    coeficientes = np.asarray(coeficientes_descendentes, dtype=float)

    if coeficientes.size == 0:
        raise ValueError("La lista de coeficientes no puede estar vacía.")

    # Filtra ceros a la izquierda para encontrar el verdadero coeficiente principal
    indices_no_ceros = np.flatnonzero(coeficientes != 0.0)
    if indices_no_ceros.size == 0:
        # Si el polinomio es completamente cero, devolvemos un radio base por defecto
        return 1.0
        
    polinomio_limpio = coeficientes[indices_no_ceros[0]:]

    # Si es un polinomio constante (grado 0), no hay raíces reales, devolvemos ventana base
    if polinomio_limpio.size == 1:
        return 1.0

    coeficiente_principal = polinomio_limpio[0]
    if coeficiente_principal == 0.0:
        return 1.0

    coeficientes_restantes = polinomio_limpio[1:]
    razones_absolutas = np.abs(coeficientes_restantes / coeficiente_principal)
    
    return float(1.0 + np.max(razones_absolutas))

def _calcular_intervalo_automatico(coeficientes_descendentes: Sequence[float], margen_relativo: float = 0.2) -> Tuple[float, float]:
    """
    Construye un intervalo [inicio, fin] automáticamente asegurando que contenga:
    - Todas las raíces de la función (usando cota de Cauchy).
    - Todos los puntos críticos (raíces de la derivada).
    """
    coeficientes = np.asarray(coeficientes_descendentes, dtype=float)
    
    # Polynomial de NumPy requiere orden ascendente [a_0, a_1, ..., a_n]
    polinomio = Polynomial(coeficientes[::-1])  
    derivada = polinomio.deriv()

    radio_funcion = _calcular_cota_cauchy(coeficientes)

    # Convertimos los coeficientes de la derivada a orden descendente para reutilizar la función de Cauchy
    coeficientes_derivada_ascendente = derivada.coef
    coeficientes_derivada_descendente = coeficientes_derivada_ascendente[::-1]
    
    if coeficientes_derivada_descendente.size > 0:
        radio_derivada = _calcular_cota_cauchy(coeficientes_derivada_descendente)
    else:
        radio_derivada = 1.0

    # Calculamos el límite máximo absoluto considerando la función y su derivada
    limite_absoluto = max(radio_funcion, radio_derivada, 1.0)
    margen_extra = (margen_relativo * limite_absoluto) + 1.0
    
    inicio_intervalo = -limite_absoluto - margen_extra
    fin_intervalo = limite_absoluto + margen_extra
    
    return inicio_intervalo, fin_intervalo

def encontrar_extremos_polinomio(coeficientes_descendentes: Sequence[float], 
    limite_inferior: float, 
    limite_superior: float) -> Tuple[float, float, float, float]:
    """
    Encuentra los mínimos y máximos absolutos de un polinomio dentro de un intervalo cerrado [a, b].
    """
    polinomio = Polynomial(coeficientes_descendentes[::-1])   
    derivada_polinomio = polinomio.deriv()

    # Los candidatos a extremos son los bordes del intervalo y los puntos críticos reales dentro del mismo
    x_candidatos = [limite_inferior, limite_superior]
    
    for raiz in derivada_polinomio.roots():
        es_raiz_real = abs(raiz.imag) < TOLERANCIA_IMAGINARIA
        if es_raiz_real:
            x_real = float(raiz.real)
            if limite_inferior <= x_real <= limite_superior:
                x_candidatos.append(x_real)

    valores_y = [polinomio(x) for x in x_candidatos]
    
    indice_minimo = int(np.argmin(valores_y))
    indice_maximo = int(np.argmax(valores_y))
    
    x_min, y_min = x_candidatos[indice_minimo], valores_y[indice_minimo]
    x_max, y_max = x_candidatos[indice_maximo], valores_y[indice_maximo]
    
    return x_min, y_min, x_max, y_max

def evaluar_polinomio(coeficientes_descendentes: Sequence[float], valor_x: float) -> float:
    """Evalúa un polinomio en un punto x específico."""
    coeficientes = np.asarray(coeficientes_descendentes, dtype=float)
    polinomio = Polynomial(coeficientes[::-1])
    return float(polinomio(valor_x))