from dataclasses import dataclass
from typing import Any

from logic.analisis.funciones_objetivo import (
    calcular_intervalo_desde_raices_y_f0,
    construir_funcion_desde_texto,
    encontrar_extremos_funcion_general,
)
from logic.metodos.metodo_secante import calcular_tabla_secante
from logic.parsing.parseo_entrada import normalizar_expresion_matematica, parsear_flotante
from logic.visualizacion.visualizacion_funcion import graficar_funcion_general


@dataclass
class SecanteResultado:
    expresion_original: str
    expresion_normalizada: str
    tabla_datos: list[dict[str, Any]]
    convergio: bool
    estado: str


def resolver_secante(
    expresion: str,
    x0_texto: str,
    x1_texto: str,
    tolerancia_texto: str,
    max_iteraciones: int,
) -> SecanteResultado:
    expresion_limpia = expresion.strip()
    if not expresion_limpia:
        raise ValueError("Debes ingresar una funcion en f(x).")

    if max_iteraciones < 1:
        raise ValueError("El maximo de iteraciones debe ser mayor a 0.")

    expresion_normalizada = normalizar_expresion_matematica(expresion_limpia)
    x0 = parsear_flotante(x0_texto)
    x1 = parsear_flotante(x1_texto)
    tolerancia = parsear_flotante(tolerancia_texto)

    if tolerancia <= 0:
        raise ValueError("La tolerancia debe ser mayor a cero.")

    funcion_objetivo = construir_funcion_desde_texto(expresion_normalizada)
    try:
        tabla_datos = calcular_tabla_secante(funcion_objetivo, x0, x1, tolerancia, max_iteraciones)
    except ValueError as error:
        raise ValueError(str(error)) from error
    convergio = bool(tabla_datos and tabla_datos[-1]["cumple_tolerancia"])

    if not tabla_datos:
        estado = "sin_iteraciones"
    elif convergio:
        estado = "convergio"
    elif len(tabla_datos) >= max_iteraciones:
        estado = "max_iteraciones"
    else:
        estado = "detenido_numerico"

    return SecanteResultado(
        expresion_original=expresion_limpia,
        expresion_normalizada=expresion_normalizada,
        tabla_datos=tabla_datos,
        convergio=convergio,
        estado=estado,
    )


def construir_figura_funcion(expresion: str):
    expresion_limpia = expresion.strip()
    if not expresion_limpia:
        raise ValueError("Debes ingresar una funcion para graficar.")

    expresion_normalizada = normalizar_expresion_matematica(expresion_limpia)
    funcion_objetivo = construir_funcion_desde_texto(expresion_normalizada)

    x_min, x_max = calcular_intervalo_desde_raices_y_f0(funcion_objetivo)
    x_minimo, y_minimo, x_maximo, y_maximo = encontrar_extremos_funcion_general(
        funcion_objetivo,
        x_min,
        x_max,
        puntos_evaluacion=3000,
    )

    return graficar_funcion_general(
        funcion_objetivo=funcion_objetivo,
        expresion_matematica=expresion_limpia,
        limite_inferior=x_min,
        limite_superior=x_max,
        x_minimo=x_minimo,
        y_minimo=y_minimo,
        x_maximo=x_maximo,
        y_maximo=y_maximo,
        mostrar=False,
    )