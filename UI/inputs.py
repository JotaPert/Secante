from pathlib import Path
import sys

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

entrada = __import__(
    "logic.entrada",
    fromlist=["normalizar_expresion_matematica", "parsear_flotante"],
)
tabla_ui = __import__("UI.tabla", fromlist=["mostrar_tabla_secante"])

normalizar_expresion_matematica = entrada.normalizar_expresion_matematica
parsear_flotante = entrada.parsear_flotante
mostrar_tabla_secante = tabla_ui.mostrar_tabla_secante

st.set_page_config(page_title="Resolucion de Ecuaciones No Lineales", layout="wide")

st.title("Metodo Secante")

with st.container(border=True):
    st.subheader("Ingrese los parámetros")

    col_izquierda, col_derecha = st.columns(2)

    with col_izquierda:
        expresion = st.text_input("Función f(x)", value="x^3 - 2x^2 - x + 2")
        x0 = st.text_input("X0", value="1")
        x1 = st.text_input("X1", value="2")

    with col_derecha:
        max_iter = st.slider("Máximo de iteraciones", min_value=1, max_value=20, value=10)
        tolerancia = st.text_input("Tolerancia de error", value="0.001")
    
    ejecutar = st.button("Ejecutar cálculo", type="primary")

if ejecutar:
    from logic.analisis_funcion import construir_funcion_desde_texto
    from logic.calcular_secante import calcular_tabla_secante

    expresion_normalizada = normalizar_expresion_matematica(expresion)
    x0_val = parsear_flotante(x0)
    x1_val = parsear_flotante(x1)
    tolerancia_val = parsear_flotante(tolerancia)

    funcion_objetivo = construir_funcion_desde_texto(expresion_normalizada)
    tabla_datos = calcular_tabla_secante(funcion_objetivo, x0_val, x1_val, tolerancia_val, max_iter)

    st.success("Cálculo completado correctamente")
    st.write("### Resumen")

    tabla_ui.mostrar_tabla_secante(tabla_datos)
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Iteraciones", len(tabla_datos))
    if tabla_datos:
        col_b.metric("Último x", f"{tabla_datos[-1]['x_n+1']:.4f}")
        col_c.metric("Último error", f"{tabla_datos[-1]['|xn - xn+1|']:.4f}")