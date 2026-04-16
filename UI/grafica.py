import streamlit as st
from app.secante_service import construir_figura_funcion


def mostrar_bloque_grafica(expresion: str, mostrar_grafica: bool) -> None:
    """
    Renderiza la grafica de la funcion cuando el usuario activa el boton.
    """
    if not mostrar_grafica:
        return

    try:
        figura = construir_figura_funcion(expresion)
        st.subheader("Grafica de la funcion")
        col_izq, col_centro, col_der = st.columns([1, 3, 1])
        with col_centro:
            st.pyplot(figura, width="content")
    except Exception as error:
        st.warning(f"No se pudo graficar la funcion. Detalle: {error}")
