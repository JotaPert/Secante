from typing import List, Dict, Callable, Union

def _calcular_siguiente_x_secante(x_actual: float, x_anterior: float, f_actual: float, f_anterior: float) -> float:
    """
    Aplica la fórmula matemática del método de la secante.
    """
    denominador = f_actual - f_anterior
    # Evita inestabilidad numerica cuando el denominador es cero (o casi cero).
    if abs(denominador) < 1e-14:
        raise ValueError(
            "No se puede aplicar el método de la secante: división por cero "
            "(o casi cero) porque f(x_n) y f(x_n-1) son iguales. "
            "Prueba con otros valores iniciales X0 y X1."
        )

    # Usamos la forma estándar de la secante para mayor estabilidad numérica
    return x_actual - f_actual * ((x_actual - x_anterior) / denominador)

def calcular_tabla_secante(
    funcion: Callable[[float], float], 
    x0: float, 
    x1: float, 
    tolerancia_error: float, 
    max_iteraciones: int = 20
) -> List[Dict[str, Union[float, bool, int]]]:
    """
    Genera los datos de la iteración del método de la secante.
    """
    tabla_datos = []
    
    x_anterior = x0
    x_actual = x1
    
    for iteracion in range(max_iteraciones):
        f_anterior = funcion(x_anterior)
        f_actual = funcion(x_actual)

        x_siguiente = _calcular_siguiente_x_secante(x_actual, x_anterior, f_actual, f_anterior)
        
        # Corregido: Calculamos el error basándonos en las X, tal como indica tu imagen |x_n - x_n+1|
    
        error_absoluto = abs(x_actual - x_siguiente)
        
        # Retornamos un booleano, es mucho más limpio para procesar después
        cumple_tolerancia = error_absoluto < tolerancia_error
        
        tabla_datos.append({
            "iteracion": iteracion + 1,
            "x_n-1": x_anterior,
            "x_n": x_actual,
            "f(x_n-1)": f_anterior,
            "f(x_n)": f_actual,
            "x_n+1": x_siguiente,
            "error_absoluto": error_absoluto,
            "cumple_tolerancia": cumple_tolerancia
        })
        
        # Si ya llegamos a la tolerancia deseada, terminamos el ciclo
        if cumple_tolerancia:
            break

        # Preparamos los valores para la siguiente iteración
        x_anterior = x_actual
        x_actual = x_siguiente
        
    return tabla_datos