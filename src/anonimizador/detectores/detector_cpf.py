import re
from collections.abc import Iterator

from anonimizador.nucleo.deteccao import Ocorrencia, coletar_ocorrencias
from anonimizador.nucleo.utils import extrair_digitos, todos_digitos_iguais


def cpf_valido(cpf: str) -> bool:
    # Recebe um CPF (com ou sem pontuação) e devolve True ou False.
    numero = extrair_digitos(cpf)

    # Verifica se tem 11 dígitos ou se é uma sequência repetida (ex: 111.111.111-11)
    if len(numero) != 11:
        return False
    if todos_digitos_iguais(numero):
        return False

    # Calcula o primeiro dígito verificador
    soma = sum(int(numero[i]) * (10 - i) for i in range(9))
    digito1 = (soma * 10) % 11
    if digito1 == 10:
        digito1 = 0
    if digito1 != int(numero[9]):
        return False

    # Calcula o segundo dígito verificador
    soma = sum(int(numero[i]) * (11 - i) for i in range(10))
    digito2 = (soma * 10) % 11
    if digito2 == 10:
        digito2 = 0
    if digito2 != int(numero[10]):
        return False

    return True


def detectar_formatos_cpf(texto: str) -> Iterator[re.Match[str]]:
    # Permite captura colada (ex: ID99-033.932.260-88)
    # sem fatiar números maiores no final
    return re.finditer(r"(?<!\d)\d{3}\.?\d{3}\.?\d{3}-?\d{2}(?!\d)", texto)


def detectar_cpfs(texto: str) -> list[Ocorrencia]:
    return coletar_ocorrencias(detectar_formatos_cpf(texto), cpf_valido)
