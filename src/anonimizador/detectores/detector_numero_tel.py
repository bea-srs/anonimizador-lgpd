from collections.abc import Iterator
import re

from anonimizador.nucleo.utils import extrair_digitos, todos_digitos_iguais
from anonimizador.nucleo.deteccao import Ocorrencia, coletar_ocorrencias

def remover_codigo_pais(digitos: str) -> str:
    # Se os dígitos começarem com 55 e tiverem 12 ou 13 dígitos, remove o DDI 55
    if digitos.startswith("55") and len(digitos) in (12, 13):
        return digitos[2:]
    return digitos


def telefone_valido(telefone: str) -> bool:
    # Recebe um telefone (com ou sem pontuação) e devolve True ou False
    numero = extrair_digitos(telefone)
    numero = remover_codigo_pais(numero)

    if len(numero) not in (10, 11):
        return False

    # Valida DDD brasileiro
    ddd = numero[:2]
    if not re.match(
        r"^(1[1-9]|2[12478]|3[1-578]|4[1-9]|5[13-5]|6[1-9]|7[13-579]|8[1-9]|9[1-9])$",
        ddd,
    ):
        return False

    # Celular com 11 dígitos (DDD + 9 + 8 dígitos)
    if len(numero) == 11 and numero[2] != "9":
        return False

    # Fixo com 10 dígitos (DDD + 2..5 + 7 dígitos)
    if len(numero) == 10 and numero[2] not in "2345":
        return False

    # Rejeita dígitos todos iguais ou sequências óbvias
    if todos_digitos_iguais(numero) or numero in (
        "12345678901",
        "01234567890",
        "98765432109",
    ):
        return False

    return True


def detectar_formatos_telefone(texto: str) -> Iterator[re.Match[str]]:
    # Aceita DDI opcional, DDD com ou sem parênteses e separadores leves
    padrao = r"(?<!\d)(?:\+?55\s*)?\(?\d{2}\)?[\s-]?\d{4,5}[\s-]?\d{4}(?!\d)"
    return re.finditer(padrao, texto)


def detectar_cpfs(texto: str) -> list[Ocorrencia]:
    return coletar_ocorrencias(detectar_formatos_telefone(texto), telefone_valido)