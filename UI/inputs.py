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

if "resultado_secante" not in st.session_state:
    st.session_state["resultado_secante"] = None

if "modo_paso_a_paso" not in st.session_state:
    st.session_state["modo_paso_a_paso"] = False

if "paso_actual" not in st.session_state:
    st.session_state["paso_actual"] = 1

st.set_page_config(page_title="Resolucion de Ecuaciones No Lineales", layout="wide")

st.markdown(
    """
    <style>
        div[data-testid="stCheckbox"] {
            margin-top: 0.35rem;
        }

        div[data-testid="stCheckbox"] > label {
            display: flex;
            align-items: center;
            gap: 0.6rem;
            transform: scale(1.15);
            transform-origin: left center;
        }

        div[data-testid="stCheckbox"] [role="checkbox"] {
            min-width: 1.25rem;
            min-height: 1.25rem;
            border-width: 2px;
        }

        div[data-testid="stCheckbox"] [data-testid="stMarkdownContainer"] p {
            font-size: 1.1rem;
            font-weight: 600;
            line-height: 1.2;
            margin: 0;
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
        st.checkbox("Mostrar grafica", key="mostrar_grafica")
        st.checkbox("Modo paso a paso", key="modo_paso_a_paso")

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

    st.session_state["resultado_secante"] = {
        "expresion": expresion,
        "tabla_datos": tabla_datos,
        "max_iter": max_iter,
        "convergio": bool(tabla_datos and tabla_datos[-1]["cumple_tolerancia"]),
    }
    st.session_state["paso_actual"] = 1 if tabla_datos else 0

resultado_secante = st.session_state.get("resultado_secante")
if resultado_secante is not None:
    tabla_datos = resultado_secante["tabla_datos"]
    convergio = resultado_secante.get("convergio", False)
    max_iter_usado = resultado_secante.get("max_iter", 0)
    total_pasos = len(tabla_datos)

    if total_pasos == 0:
        st.warning("No se generaron iteraciones. Revisa los valores iniciales.")
    elif convergio:
        st.success("El método alcanzó la tolerancia indicada.")
    elif total_pasos >= max_iter_usado:
        st.warning(
            "No se alcanzó la tolerancia antes del máximo de iteraciones. "
            "Puedes aumentar iteraciones, relajar tolerancia o ajustar X0/X1."
        )
    else:
        st.info("El método se detuvo por una condición numérica (por ejemplo, división por cero).")

    if st.session_state["modo_paso_a_paso"] and total_pasos > 0:
        col_info, col_accion_1, col_accion_2 = st.columns([2, 1, 1])

        paso_actual = max(1, min(st.session_state["paso_actual"], total_pasos))

        with col_info:
            st.info(f"Paso actual: {paso_actual} de {total_pasos}")

        with col_accion_1:
            if st.button("Siguiente paso", disabled=paso_actual >= total_pasos):
                st.session_state["paso_actual"] = min(total_pasos, paso_actual + 1)

        with col_accion_2:
            if st.button("Reiniciar pasos"):
                st.session_state["paso_actual"] = 1

        paso_actual = max(1, min(st.session_state["paso_actual"], total_pasos))
        mostrar_tabla_secante(tabla_datos[:paso_actual])
        fila_referencia = tabla_datos[paso_actual - 1]
    else:
        mostrar_tabla_secante(tabla_datos)
        fila_referencia = tabla_datos[-1] if tabla_datos else None

    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Iteraciones", len(tabla_datos))
    if fila_referencia is not None:
        col_b.metric("x mostrado", f"{fila_referencia['x_n+1']:.4f}")
        col_c.metric("Error mostrado", f"{fila_referencia['error_absoluto']:.4f}")

expresion_para_grafica = expresion
if resultado_secante is not None:
    expresion_para_grafica = resultado_secante["expresion"]

mostrar_bloque_grafica(
    expresion=expresion_para_grafica,
    mostrar_grafica=st.session_state["mostrar_grafica"],
)