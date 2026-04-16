import pandas as pd
import streamlit as st


def formatear_tabla_secante(tabla_datos):
    """
    Convierte la lista de diccionarios del metodo de la secante en una tabla
    mas limpia para mostrar en Streamlit.
    """
    if not tabla_datos:
        return pd.DataFrame(
            columns=[
                "x_n-1",
                "x_n",
                "f(x_n-1)",
                "f(x_n)",
                "x_n+1",
                "|xn - xn+1|",
                "Cumple tolerancia",
            ]
        )

    datos = []
    for fila in tabla_datos:
        datos.append(
            {
                "x_n-1": round(fila["x_n-1"], 4),
                "x_n": round(fila["x_n"], 4),
                "f(x_n-1)": round(fila["f(x_n-1)"], 4),
                "f(x_n)": round(fila["f(x_n)"], 4),
                "x_n+1": round(fila["x_n+1"], 4),
                "|xn - xn+1|": round(fila["error_absoluto"], 4),
                "Cumple tolerancia": "Sí" if fila["cumple_tolerancia"] else "No",
            }
        )

    return pd.DataFrame(datos)


def mostrar_tabla_secante(tabla_datos):
    """
    Renderiza la tabla del metodo de la secante con estilo visual simple.
    """
    df = formatear_tabla_secante(tabla_datos)

    st.markdown(
        """
        <style>
            div[data-testid="stDataFrame"] {
                border-radius: 14px;
                overflow: hidden;
                border: 1px solid rgba(148, 163, 184, 0.25);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.dataframe(
        df,
        width="stretch",
        hide_index=True,
    )
