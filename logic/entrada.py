import re


def normalizar_expresion_matematica(expresion: str) -> str:
    """
    Normaliza una expresion matematica para que Python pueda evaluarla.

    Convierte:
    - '^' en '**'
    - multiplicacion implicita como '3x' o '2(x+1)' en multiplicacion explicita
    """
    texto = expresion.strip().replace("^", "**")

    texto = re.sub(r"(?<=\d)(?=x)", "*", texto)
    texto = re.sub(r"(?<=x)(?=\()", "*", texto)
    texto = re.sub(r"(?<=\d)(?=\()", "*", texto)
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