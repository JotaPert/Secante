from pathlib import Path
import sys
import importlib

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
	sys.path.insert(0, str(ROOT_DIR))

analisis = __import__(
	"logic.analisis_funcion",
	fromlist=[
		"construir_funcion_desde_texto",
		"calcular_intervalo_desde_raices_y_f0",
		"encontrar_extremos_funcion_general",
	],
)
entrada = __import__("logic.entrada", fromlist=["normalizar_expresion_matematica"])
grafica_logic = __import__("logic.grafica", fromlist=["graficar_funcion_general"])

# Evita usar una version antigua del modulo durante recargas de Streamlit.
grafica_logic = importlib.reload(grafica_logic)

## Construcción de funciones y gráficas
construir_funcion_desde_texto = analisis.construir_funcion_desde_texto
calcular_intervalo_desde_raices_y_f0 = analisis.calcular_intervalo_desde_raices_y_f0
encontrar_extremos_funcion_general = analisis.encontrar_extremos_funcion_general
normalizar_expresion_matematica = entrada.normalizar_expresion_matematica
graficar_funcion_general = grafica_logic.graficar_funcion_general


def mostrar_bloque_grafica(expresion: str, mostrar_grafica: bool) -> None:
	"""
	Renderiza la grafica de la funcion cuando el usuario activa el boton.
	"""
	if not mostrar_grafica:
		return

	try:
		expresion_normalizada = normalizar_expresion_matematica(expresion)
		funcion_objetivo = construir_funcion_desde_texto(expresion_normalizada)

		x_min, x_max = calcular_intervalo_desde_raices_y_f0(funcion_objetivo)
		x_minimo, y_minimo, x_maximo, y_maximo = encontrar_extremos_funcion_general(
			funcion_objetivo,
			x_min,
			x_max,
			puntos_evaluacion=3000,
		)

		figura = graficar_funcion_general(
			funcion_objetivo=funcion_objetivo,
			expresion_matematica=expresion,
			limite_inferior=x_min,
			limite_superior=x_max,
			x_minimo=x_minimo,
			y_minimo=y_minimo,
			x_maximo=x_maximo,
			y_maximo=y_maximo,
			mostrar=False,
		)

		st.subheader("Grafica de la funcion")
		col_izq, col_centro, col_der = st.columns([1, 3, 1])
		with col_centro:
			st.pyplot(figura, width="content")
	except Exception as error:
		st.warning(f"No se pudo graficar la funcion. Detalle: {error}")
