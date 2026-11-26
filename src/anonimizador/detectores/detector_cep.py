from collections.abc import Iterator
import re

from anonimizador.nucleo.utils import extrair_digitos, todos_digitos_iguais
from anonimizador.nucleo.deteccao import Ocorrencia, coletar_ocorrencias

def cep_valido(cep: str) -> bool:
    numero = extrair_digitos(cep)
    return len(numero) == 8 and not todos_digitos_iguais(numero)


def detectar_por_formato(texto: str) -> Iterator[re.Match[str]]:
    # Detecção com formato XXXXX-XXX sem bloquear prefixos como "ID99-"
    return re.finditer(r"(?<!\d)(?<!\d[.-])\d{5}-\d{3}(?!\d)(?![.-]\d)", texto)


def detectar_por_palavra(texto: str) -> Iterator[re.Match[str]]:
    # Detecção pelas palavras cep, zip, zipcode, código ou codigo postal
    # Aceita XXXXX-XXX ou XXXXXXXX quando há palavra-chave válida antes
    return re.finditer(
        r"(?i)\b(?:cep|zip|zip\s?code|c[oó]digo\s?postal)\b\W{0,5}(?<!\d[.-])(\d{5}-?\d{3})(?!\d)(?![.-]\d)",
        texto,
    )

def detectar_ceps(texto: str) -> list[Ocorrencia]:
    por_formato = coletar_ocorrencias(detectar_por_formato(texto), cep_valido)
    por_palavra = coletar_ocorrencias(detectar_por_palavra(texto), cep_valido, grupo=1)
    return sorted(set(por_formato + por_palavra), key=lambda o: o[1])