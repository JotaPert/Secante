# Método de la Secante

Aplicación en Python desarrollada con Streamlit para aproximar raíces de ecuaciones no lineales mediante el método de la secante.

La app permite ingresar una función $f(x)$, dos valores iniciales, una tolerancia y un máximo de iteraciones. Luego calcula la tabla de iteraciones, muestra una raíz aproximada y, si se desea, grafica la función.

## Características

- Cálculo del método de la secante paso a paso.
- Tabla con cada iteración, valores intermedios y error absoluto.
- Indicadores del estado del cálculo: convergencia, máximo de iteraciones o detención numérica.
- Opción para visualizar la gráfica de la función.
- Interfaz simple en español pensada para uso educativo.

## Proximamente 

- Método Resolucion de Ecuaciones No Lineales - BISECCION
-  Método Resolucion de Ecuaciones No Lineales - NEWTON

## Requisitos

- Python 3.11
- Streamlit
- NumPy
- Pandas
- Matplotlib

Las dependencias están listadas en `requirements.txt`.

## Instalación

1. Clona el repositorio.
2. Crea y activa un entorno virtual.
3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución

Para iniciar la aplicación localmente:

```bash
streamlit run streamlit_app.py
```

## Cómo usar la app

1. Escribe la función en el campo `Función f(x)`.
2. Ingresa los valores iniciales `X0` y `X1`.
3. Define la tolerancia de error.
4. Ajusta el máximo de iteraciones.
5. Presiona `Ejecutar cálculo`.

Si activas `Mostrar gráfica`, la aplicación intentará dibujar la función ingresada.

## Formato de entrada

La app acepta expresiones matemáticas comunes. Algunos ejemplos:

- `x^3 - 2x^2 - x + 2`
- `x^2 - 4`
- `3/2`
- `2(x+1)`

También normaliza algunas variantes frecuentes como:

- `X` como variable equivalente a `x`
- `^` como potencia
- multiplicación implícita, por ejemplo `2x` o `3(x+1)`
- fracciones en los valores iniciales, por ejemplo `3/2`

## Interpretación de resultados

La tabla muestra, para cada iteración:

- `x_n-1` y `x_n`
- `f(x_n-1)` y `f(x_n)`
- `x_n+1`
- el error absoluto `|xn - xn+1|`
- si la iteración cumple la tolerancia

Además, la interfaz muestra métricas resumidas como:

- cantidad de iteraciones realizadas
- raíz aproximada
- error mostrado en la última fila disponible

## Estructura del proyecto

- `streamlit_app.py`: punto de entrada para Streamlit.
- `app/`: lógica de orquestación entre interfaz y cálculo.
- `logic/metodos/`: implementación del método numérico.
- `logic/parsing/`: normalización y validación de entradas.
- `logic/visualizacion/`: generación de gráficas.
- `ui/`: componentes visuales de la aplicación.

