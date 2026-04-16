from app.secante_service import construir_figura_funcion, resolver_secante


def _imprimir_tabla_secante_consola(tabla_datos: list[dict]) -> None:
    if not tabla_datos:
        print("No se generaron iteraciones.")
        return

    encabezados = [
        "iter",
        "x_n-1",
        "x_n",
        "f(x_n-1)",
        "f(x_n)",
        "x_n+1",
        "error",
        "tol",
    ]
    print(" | ".join(encabezados))
    print("-" * 92)
    for fila in tabla_datos:
        print(
            " | ".join(
                [
                    str(fila["iteracion"]),
                    f"{fila['x_n-1']:.6f}",
                    f"{fila['x_n']:.6f}",
                    f"{fila['f(x_n-1)']:.6f}",
                    f"{fila['f(x_n)']:.6f}",
                    f"{fila['x_n+1']:.6f}",
                    f"{fila['error_absoluto']:.6f}",
                    "si" if fila["cumple_tolerancia"] else "no",
                ]
            )
        )


def ejecutar_modo_interactivo() -> None:
    """
    Punto de entrada para que el usuario ingrese la funcion por consola.
    Coordina los calculos y llama a la funcion de graficado.
    """
    expresion_usuario = input("f(x) = ").strip()

    if not expresion_usuario:
        print("No ingresaste una funcion valida.")
        return

    try:
        x0 = input().strip()
        x1 = input().strip()
        tolerancia_error = input().strip()
        max_iteraciones = int(input().strip())

        resultado = resolver_secante(
            expresion=expresion_usuario,
            x0_texto=x0,
            x1_texto=x1,
            tolerancia_texto=tolerancia_error,
            max_iteraciones=max_iteraciones,
        )

        _imprimir_tabla_secante_consola(resultado.tabla_datos)
        figura = construir_figura_funcion(resultado.expresion_original)
        if figura is not None:
            figura.show()

    except Exception as error:
        print(f"No se pudo interpretar o calcular la funcion. Detalle del error: {error}")


def render_streamlit_app() -> None:
    import streamlit as st
    from UI.tabla import mostrar_tabla_secante

    st.set_page_config(page_title="Resolucion de Ecuaciones No Lineales", layout="wide")

    if "mostrar_grafica" not in st.session_state:
        st.session_state["mostrar_grafica"] = False
    if "resultado_secante" not in st.session_state:
        st.session_state["resultado_secante"] = None
    if "modo_paso_a_paso" not in st.session_state:
        st.session_state["modo_paso_a_paso"] = False
    if "paso_actual" not in st.session_state:
        st.session_state["paso_actual"] = 1

    st.title("Metodo Secante")

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

    if ejecutar:
        try:
            resultado = resolver_secante(
                expresion=expresion,
                x0_texto=x0,
                x1_texto=x1,
                tolerancia_texto=tolerancia,
                max_iteraciones=max_iter,
            )
            st.session_state["resultado_secante"] = resultado
            st.session_state["paso_actual"] = 1 if resultado.tabla_datos else 0
        except Exception as error:
            st.session_state["resultado_secante"] = None
            st.error(f"No se pudo ejecutar el metodo. Detalle: {error}")

    resultado = st.session_state.get("resultado_secante")
    if resultado is not None:
        tabla_datos = resultado.tabla_datos
        total_pasos = len(tabla_datos)

        if resultado.estado == "sin_iteraciones":
            st.warning("No se generaron iteraciones. Revisa los valores iniciales.")
        elif resultado.estado == "convergio":
            st.success("El metodo alcanzo la tolerancia indicada.")
        elif resultado.estado == "max_iteraciones":
            st.warning(
                "No se alcanzo la tolerancia antes del maximo de iteraciones. "
                "Puedes aumentar iteraciones, relajar tolerancia o ajustar X0/X1."
            )
        else:
            st.info("El metodo se detuvo por una condicion numerica.")

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

    if st.session_state["mostrar_grafica"]:
        expresion_grafica = expresion
        if resultado is not None:
            expresion_grafica = resultado.expresion_original

        try:
            figura = construir_figura_funcion(expresion_grafica)
            st.subheader("Grafica de la funcion")
            col_izq, col_centro, col_der = st.columns([1, 3, 1])
            with col_centro:
                st.pyplot(figura, width="content")
        except Exception as error:
            st.warning(f"No se pudo graficar la funcion. Detalle: {error}")
