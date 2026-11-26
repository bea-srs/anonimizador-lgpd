import re
from collections.abc import Iterator

from anonimizador.nucleo.deteccao import Ocorrencia, coletar_ocorrencias


def detectar_formato_emails(texto: str) -> Iterator[re.Match[str]]:
    padrao = (
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+"
        r"(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}(?![\w-])(?!\.\w)"
    )
    return re.finditer(padrao, texto)


def detectar_emails(texto: str) -> list[Ocorrencia]:
    return coletar_ocorrencias(detectar_formato_emails(texto))
