import streamlit as st

st.set_page_config(page_title="Metodo Secante", layout="wide")

st.title("Vista de Inputs")
st.caption("Prueba rápida para ver cómo se ven distintos componentes en Streamlit.")

with st.container(border=True):
    st.subheader("Formulario de ejemplo")

    col_izquierda, col_derecha = st.columns(2)

    with col_izquierda:
        expresion = st.text_input("Función f(x)", value="x**3 - 2*x**2 - x + 2")
        x0 = st.number_input("X0", value=1.0, step=0.1, format="%.3f")
        x1 = st.number_input("X1", value=2.0, step=0.1, format="%.3f")

    with col_derecha:
        max_iter = st.slider("Máximo de iteraciones", min_value=1, max_value=100, value=20)
        mostrar_tabla = st.checkbox("Mostrar tabla de iteraciones", value=True)
        tolerancia = st.number_input("Tolerancia de error", value=0.001, min_value=0.0, step=0.0001, format="%.3f")


    ejecutar = st.button("Ejecutar cálculo", type="primary")
