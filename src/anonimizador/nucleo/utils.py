import re


def extrair_digitos(texto: str) -> str:
    """Retorna apenas os caracteres numéricos de uma string."""
    return re.sub(r"\D", "", texto)


def todos_digitos_iguais(digitos: str) -> bool:
    """Verifica se uma sequência não vazia é composta por um único dígito repetido."""
    return bool(digitos) and digitos == digitos[0] * len(digitos)