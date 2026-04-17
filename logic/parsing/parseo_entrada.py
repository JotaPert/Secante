import re


def normalizar_expresion_matematica(expresion: str) -> str:
    """
    Normaliza una expresion matematica para que Python pueda evaluarla.

    Convierte:
    - '^' en '**'
    - multiplicacion implicita como '3x' o '2(x+1)' en multiplicacion explicita
    """
    texto = expresion.strip()

    # Normaliza variantes comunes que vienen de teclado/copia y pega.
    reemplazos_simbolos = {
        "X": "x",
        "×": "*",
        "÷": "/",
        "−": "-",
        "–": "-",
        "—": "-",
    }
    for origen, destino in reemplazos_simbolos.items():
        texto = texto.replace(origen, destino)

    # Soporte para superindices Unicode frecuentes: x², x³, etc.
    superindices = {
        "⁰": "0",
        "¹": "1",
        "²": "2",
        "³": "3",
        "⁴": "4",
        "⁵": "5",
        "⁶": "6",
        "⁷": "7",
        "⁸": "8",
        "⁹": "9",
    }
    texto = re.sub(r"([)x\d])([⁰¹²³⁴⁵⁶⁷⁸⁹]+)", lambda m: f"{m.group(1)}**{''.join(superindices[c] for c in m.group(2))}", texto)

    texto = texto.replace("^", "**")

    texto = re.sub(r"(?<=\d)(?=x)", "*", texto)
    texto = re.sub(r"(?<=x)(?=\()", "*", texto)
    texto = re.sub(r"(?<=\d)(?=\()", "*", texto)
    texto = re.sub(r"(?<=\d)(?=[a-zA-Z])", "*", texto)
    texto = re.sub(r"(?<=\))(?=\d|x|\()", "*", texto)
    texto = re.sub(r"(?<=x)(?=\d)", "*", texto)

    return texto


def parsear_flotante(valor_texto: str) -> float:
    """
    Convierte texto a float aceptando formatos como '1.5' o fracciones '3/2'.
    """
    texto = valor_texto.strip()
    if not texto:
        raise ValueError("entrada vacia")

    if "/" in texto:
        partes = texto.split("/")
        if len(partes) != 2:
            raise ValueError(f"fraccion invalida: '{valor_texto}'")

        numerador = float(partes[0].strip())
        denominador = float(partes[1].strip())
        if denominador == 0:
            raise ValueError("el denominador no puede ser cero")
        return numerador / denominador

    return float(texto)