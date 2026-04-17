import streamlit as st
from app.secante_service import construir_figura_funcion


def mostrar_bloque_grafica(expresion: str, mostrar_grafica: bool) -> None:
    """
    Renderiza la gráfica de la función cuando el usuario activa el botón.
    """
    if not mostrar_grafica:
        return

    try:
        figura = construir_figura_funcion(expresion)
        st.subheader("Gráfica de la función")
        col_izq, col_centro, col_der = st.columns([1, 3, 1])
        with col_centro:
            st.pyplot(figura, width="content")
    except ValueError as error:
        st.warning(f"No se pudo graficar la función: {error}")
    except Exception:
        st.warning("No se pudo graficar la función por un error inesperado.")
