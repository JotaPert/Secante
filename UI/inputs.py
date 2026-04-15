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

normalizar_expresion_matematica = entrada.normalizar_expresion_matematica
parsear_flotante = entrada.parsear_flotante

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
        max_iter = st.slider("Máximo de iteraciones", min_value=1, max_value=100, value=20)
        mostrar_tabla = st.checkbox("Mostrar tabla de iteraciones", value=True)
        tolerancia = st.text_input("Tolerancia de error", value="0.001")


    ejecutar = st.button("Ejecutar cálculo", type="primary")

if ejecutar:
    expresion_normalizada = normalizar_expresion_matematica(expresion)
    x0_val = parsear_flotante(x0)
    x1_val = parsear_flotante(x1)
    tolerancia_val = parsear_flotante(tolerancia)

    st.success("Inputs capturados correctamente")
    st.write("### Valores actuales")
    st.json(
        {
            "expresion": expresion,
            "x0": x0_val,
            "x1": x1_val,
            "tolerancia": tolerancia_val,
            "max_iteraciones": max_iter,
            "mostrar_tabla": mostrar_tabla,
        }
    )
