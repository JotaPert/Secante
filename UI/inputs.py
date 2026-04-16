import streamlit as st

def render_formulario_secante() -> tuple[dict[str, str | int], bool]:
    """
    Renderiza los controles de entrada y devuelve sus valores junto con el estado del boton.
    """
    with st.container(border=True):
        st.subheader("Ingrese los parametros")

        col_izquierda, col_derecha = st.columns(2)

        with col_izquierda:
            expresion = st.text_input("Funcion f(x)", placeholder="x^3 - 2x^2 - x + 2", value="x^3 - 2x^2 - x + 2")
            x0 = st.text_input("X0", placeholder="0", value="0")
            x1 = st.text_input("X1", placeholder="3/2", value="3/2")

        with col_derecha:
            max_iter = st.slider("Maximo de iteraciones", min_value=1, max_value=20, value=10)
            tolerancia = st.text_input("Tolerancia de error", placeholder="0.1", value="0.1")
            st.checkbox("Mostrar grafica", key="mostrar_grafica")
            st.checkbox("Modo paso a paso", key="modo_paso_a_paso")

        ejecutar = st.button("Ejecutar calculo", type="primary")

    return {
        "expresion": expresion,
        "x0": x0,
        "x1": x1,
        "max_iter": max_iter,
        "tolerancia": tolerancia,
    }, ejecutar