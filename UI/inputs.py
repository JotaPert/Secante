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
grafica_ui = __import__("UI.grafica", fromlist=["mostrar_bloque_grafica"])

## Construcción de funciones y gráficas
normalizar_expresion_matematica = entrada.normalizar_expresion_matematica
parsear_flotante = entrada.parsear_flotante
mostrar_tabla_secante = tabla_ui.mostrar_tabla_secante
mostrar_bloque_grafica = grafica_ui.mostrar_bloque_grafica

if "mostrar_grafica" not in st.session_state:
    st.session_state["mostrar_grafica"] = False

st.set_page_config(page_title="Resolucion de Ecuaciones No Lineales", layout="wide")

st.markdown(
    """
    <style>
        div[data-testid="stButton"] > button[kind="secondary"] {
            margin-top: 10px;
            border: 1px solid #dc2626;
            color: #ffffff;
            background: #dc2626;
            font-weight: 600;
        }
        div[data-testid="stButton"] > button[kind="secondary"]:hover {
            border-color: #b91c1c;
            color: #ffffff;
            background: #b91c1c;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Metodo Secante")

with st.container(border=True):
    st.subheader("Ingrese los parámetros")

    col_izquierda, col_derecha = st.columns(2)

    with col_izquierda:
        expresion = st.text_input("Función f(x)", placeholder="x^3 - 2x^2 - x + 2", value="x^3 - 2x^2 - x + 2")
        x0 = st.text_input("X0", placeholder="0", value="0")
        x1 = st.text_input("X1", placeholder="3/2", value="3/2")

    with col_derecha:
        max_iter = st.slider("Máximo de iteraciones", min_value=1, max_value=20, value=10)
        tolerancia = st.text_input("Tolerancia de error", placeholder="0.1", value="0.1")
        if st.button("Mostrar grafica", type="secondary", use_container_width=True):
            st.session_state["mostrar_grafica"] = True

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

    tabla_ui.mostrar_tabla_secante(tabla_datos)
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Iteraciones", len(tabla_datos))
    if tabla_datos:
        col_b.metric("Último x", f"{tabla_datos[-1]['x_n+1']:.4f}")
        col_c.metric("Último error", f"{tabla_datos[-1]['error_absoluto']:.4f}")

mostrar_bloque_grafica(
    expresion=expresion,
    mostrar_grafica=st.session_state["mostrar_grafica"],
)