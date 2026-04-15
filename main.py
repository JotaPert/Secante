from funciones_generales import (
    construir_funcion_desde_texto,
    calcular_intervalo_desde_raices_y_f0,
    encontrar_extremos_funcion_general,
)
from grafica import graficar_funcion_general



def ejecutar_modo_interactivo() -> None:
    """
    Punto de entrada para que el usuario ingrese la función por consola.
    Coordina los cálculos y llama a la función de graficado.
    """
    print("Escribe tu función usando 'x'.")
    print("Ejemplos: x**3 - 6*x**2 + 11*x - 6   |   x**3 - x**2 + 13*x - 1")
    expresion_usuario = input("f(x) = ").strip()

    if not expresion_usuario:
        print("No ingresaste una función válida.")
        return

    try:
        funcion_objetivo = construir_funcion_desde_texto(expresion_usuario)

        # 1. Calculamos la ventana de análisis dinámicamente
        x_min, x_max = calcular_intervalo_desde_raices_y_f0(funcion_objetivo)

        # 2. Encontramos los extremos numéricamente
        x_minimo, y_minimo, x_maximo, y_maximo = encontrar_extremos_funcion_general(
            funcion_objetivo, x_min, x_max, puntos_evaluacion=3000
        )

        # 3. Mostramos resultados por consola
        print(f"\nResultados aproximados en el intervalo [{x_min:.2f}, {x_max:.2f}]:")
        print(f"Mínimo: x = {x_minimo:.4f}, y = {y_minimo:.4f}")
        print(f"Máximo: x = {x_maximo:.4f}, y = {y_maximo:.4f}")

        # 4. Delegamos la visualización a su función específica
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
        print(f"No se pudo interpretar o calcular la función. Detalle del error: {error}")


if __name__ == "__main__":
    ejecutar_modo_interactivo()