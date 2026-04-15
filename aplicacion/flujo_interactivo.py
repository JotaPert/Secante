from analisis_funcion import (
    construir_funcion_desde_texto,
    calcular_intervalo_desde_raices_y_f0,
    encontrar_extremos_funcion_general,
)
from grafica import graficar_funcion_general
from calcular_secante import imprimir_tabla_secante, calcular_tabla_secante


def _parsear_flotante(valor_texto: str) -> float:
    """
    Convierte texto a float aceptando formatos como '1.5' o fracciones '3/2'.
    """
    texto = valor_texto.strip()
    if not texto:
        raise ValueError("entrada vacia")

    if "/" in texto:
        partes = texto.split("/")
        if len(partes) != 2:
            raise ValueError(f"fraccion invalida: '{valor_texto}'")

        numerador = float(partes[0].strip())
        denominador = float(partes[1].strip())
        if denominador == 0:
            raise ValueError("el denominador no puede ser cero")
        return numerador / denominador

    return float(texto)


def ejecutar_modo_interactivo() -> None:
    """
    Punto de entrada para que el usuario ingrese la funcion por consola.
    Coordina los calculos y llama a la funcion de graficado.
    """
    print("Escribe tu funcion usando 'x'.")
    print("Ejemplos: x**3 - 6*x**2 + 11*x - 6   |   x**3 - 2*x**2 - x + 2")
    expresion_usuario = input("f(x) = ").strip()

    if not expresion_usuario:
        print("No ingresaste una funcion valida.")
        return

    try:
        funcion_objetivo = construir_funcion_desde_texto(expresion_usuario)

        print("Escribe X0:")
        x0 = _parsear_flotante(input())
        print("Escribe X1:")
        x1 = _parsear_flotante(input())
        print("Escribe la tolerancia de error:")
        tolerancia_error = _parsear_flotante(input())
        print("Escribe el numero maximo de iteraciones:")
        max_iteraciones = int(input().strip())

        tabla_datos = calcular_tabla_secante(funcion_objetivo, x0, x1, tolerancia_error, max_iteraciones)
        imprimir_tabla_secante(tabla_datos)

        # 1. Calculamos la ventana de analisis dinamicamente
        x_min, x_max = calcular_intervalo_desde_raices_y_f0(funcion_objetivo)

        # 2. Encontramos los extremos numericamente
        x_minimo, y_minimo, x_maximo, y_maximo = encontrar_extremos_funcion_general(
            funcion_objetivo, x_min, x_max, puntos_evaluacion=3000
        )

        # 3. Mostramos resultados por consola
        print(f"\nResultados aproximados en el intervalo [{x_min:.2f}, {x_max:.2f}]:")
        print(f"Minimo: x = {x_minimo:.4f}, y = {y_minimo:.4f}")
        print(f"Maximo: x = {x_maximo:.4f}, y = {y_maximo:.4f}")

        # 4. Delegamos la visualizacion a su funcion especifica
        graficar_funcion_general(
            funcion_objetivo=funcion_objetivo,
            expresion_matematica=expresion_usuario,
            limite_inferior=x_min,
            limite_superior=x_max,
            x_minimo=x_minimo,
            y_minimo=y_minimo,
            x_maximo=x_maximo,
            y_maximo=y_maximo
        )

    except Exception as error:
        print(f"No se pudo interpretar o calcular la funcion. Detalle del error: {error}")
