from logic.analisis_funcion import (
    construir_funcion_desde_texto,
    calcular_intervalo_desde_raices_y_f0,
    encontrar_extremos_funcion_general,
)
from logic.grafica import graficar_funcion_general
from logic.calcular_secante import imprimir_tabla_secante, calcular_tabla_secante
from logic.entrada import normalizar_expresion_matematica, parsear_flotante


def ejecutar_modo_interactivo() -> None:
    """
    Punto de entrada para que el usuario ingrese la funcion por consola.
    Coordina los calculos y llama a la funcion de graficado.
    """
    expresion_usuario = input("f(x) = ").strip()

    if not expresion_usuario:
        print("No ingresaste una funcion valida.")
        return

    try:
        expresion_normalizada = normalizar_expresion_matematica(expresion_usuario)
        funcion_objetivo = construir_funcion_desde_texto(expresion_normalizada)

        x0 = parsear_flotante(input())
        x1 = parsear_flotante(input())
        tolerancia_error = parsear_flotante(input())
        max_iteraciones = int(input().strip())

        tabla_datos = calcular_tabla_secante(funcion_objetivo, x0, x1, tolerancia_error, max_iteraciones)
        imprimir_tabla_secante(tabla_datos)

        # 1. Calculamos la ventana de analisis dinamicamente
        x_min, x_max = calcular_intervalo_desde_raices_y_f0(funcion_objetivo)

        # 2. Encontramos los extremos numericamente
        x_minimo, y_minimo, x_maximo, y_maximo = encontrar_extremos_funcion_general(
            funcion_objetivo, x_min, x_max, puntos_evaluacion=3000
        )


        # 4. Delegamos la visualizacion a su funcion especifica
        graficar_funcion_general(
            funcion_objetivo=funcion_objetivo,
            expresion_matematica=expresion_normalizada,
            limite_inferior=x_min,
            limite_superior=x_max,
            x_minimo=x_minimo,
            y_minimo=y_minimo,
            x_maximo=x_maximo,
            y_maximo=y_maximo
        )

    except Exception as error:
        print(f"No se pudo interpretar o calcular la funcion. Detalle del error: {error}")
