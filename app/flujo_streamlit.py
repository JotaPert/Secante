import streamlit as st

from app.secante_service import resolver_secante
from ui.grafica import mostrar_bloque_grafica
from ui.inputs import render_formulario_secante
from ui.tabla import mostrar_tabla_secante


def _inicializar_estado() -> None:
    if "mostrar_grafica" not in st.session_state:
        st.session_state["mostrar_grafica"] = False
    if "resultado_secante" not in st.session_state:
        st.session_state["resultado_secante"] = None
    if "modo_paso_a_paso" not in st.session_state:
        st.session_state["modo_paso_a_paso"] = False
    if "paso_actual" not in st.session_state:
        st.session_state["paso_actual"] = 1


def _mostrar_estado_resultado(resultado) -> None:
    if resultado.estado == "sin_iteraciones":
        st.warning("No se generaron iteraciones. Revisa los valores iniciales.")
    elif resultado.estado == "convergio":
        st.success("El método alcanzó la tolerancia indicada.")
    elif resultado.estado == "max_iteraciones":
        st.warning(
            "No se alcanzó la tolerancia antes del máximo de iteraciones. "
            "Puedes aumentar iteraciones, relajar tolerancia o ajustar X0/X1."
        )
    else:
        st.info("El método se detuvo por una condición numérica.")


def _mostrar_resumen_iterativo(tabla_datos: list[dict], total_pasos: int) -> dict | None:
    if st.session_state["modo_paso_a_paso"] and total_pasos > 0:
        col_info, col_accion_1, col_accion_2 = st.columns([2, 1, 1])

        paso_actual = max(1, min(st.session_state["paso_actual"], total_pasos))
        with col_info:
            st.info(f"Paso actual: {paso_actual} de {total_pasos}")
        with col_accion_1:
            if st.button("Siguiente paso", key="btn_siguiente_paso", disabled=paso_actual >= total_pasos):
                st.session_state["paso_actual"] = min(total_pasos, paso_actual + 1)
                st.rerun()
        with col_accion_2:
            if st.button("Reiniciar pasos", key="btn_reiniciar_pasos"):
                st.session_state["paso_actual"] = 1
                st.rerun()

        paso_actual = max(1, min(st.session_state["paso_actual"], total_pasos))
        mostrar_tabla_secante(tabla_datos[:paso_actual])
        return tabla_datos[paso_actual - 1]

    mostrar_tabla_secante(tabla_datos)
    return tabla_datos[-1] if tabla_datos else None


def render_streamlit_app() -> None:
    st.set_page_config(page_title="Resolucion de Ecuaciones No Lineales", layout="wide")

    st.markdown(
        """
        <style>
            div[data-testid="stCheckbox"] {
                margin: 0.35rem 0 0.55rem 0;
            }

            div[data-testid="stCheckbox"] > label:hover {
                border-color: rgba(59, 130, 246, 0.5);
                box-shadow: 0 2px 10px rgba(59, 130, 246, 0.14);
                transform: translateY(-1px);
            }

            div[data-testid="stCheckbox"] [role="checkbox"] {
                min-width: 1.1rem;
                min-height: 1.1rem;
                border-width: 2px;
            }

            div[data-testid="stCheckbox"] [data-testid="stMarkdownContainer"] p {
                font-size: 1rem;
                font-weight: 600;
                margin: 0;
                line-height: 1.2;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    _inicializar_estado()

    st.title("Método Secante")

    expresion, ejecutar = render_formulario_secante()

    if ejecutar:
        try:
            resultado = resolver_secante(
                expresion=expresion["expresion"],
                x0_texto=expresion["x0"],
                x1_texto=expresion["x1"],
                tolerancia_texto=expresion["tolerancia"],
                max_iteraciones=expresion["max_iter"],
            )
            st.session_state["resultado_secante"] = resultado
            st.session_state["paso_actual"] = 1 if resultado.tabla_datos else 0
        except Exception as error:
            st.session_state["resultado_secante"] = None
            st.error(f"No se pudo ejecutar el método. Detalle: {error}")

    resultado = st.session_state.get("resultado_secante")
    fila_referencia = None

    if resultado is not None:
        tabla_datos = resultado.tabla_datos
        total_pasos = len(tabla_datos)

        _mostrar_estado_resultado(resultado)
        fila_referencia = _mostrar_resumen_iterativo(tabla_datos, total_pasos)

        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Iteraciones", len(tabla_datos))
        if fila_referencia is not None:
            col_b.metric("Raíz aproximada", f"{fila_referencia['x_n+1']:.4f}")
            col_c.metric("Error mostrado", f"{fila_referencia['error_absoluto']:.4f}")

    if st.session_state["mostrar_grafica"]:
        expresion_grafica = expresion["expresion"]
        if resultado is not None:
            expresion_grafica = resultado.expresion_original
        mostrar_bloque_grafica(expresion_grafica, True)