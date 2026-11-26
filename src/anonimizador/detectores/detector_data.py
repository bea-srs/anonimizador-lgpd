from collections.abc import Iterator
from datetime import date
import re

from anonimizador.nucleo.deteccao import Ocorrencia, coletar_ocorrencias


# Compilado uma vez só (mais eficiente que recompilar a cada chamada).
# ^ e $ exigem que a string INTEIRA seja uma data, sem texto sobrando.
# Alternativa 1 (grupos 1-3): dia, mês, ano com 4 ou 2 dígitos, ex: 15/05/1990 ou 15.05.90
# Alternativa 2 (grupos 4-6): ano com 4 dígitos primeiro, ex: 1990-05-15 (ISO 8601)
# [/.-] aceita barra, ponto ou hífen como separador

def detectar_formato_data(texto: str) -> Iterator[str]:
    PADRAO_DATA = re.compile(
    r"^(?:(\d{1,2})[/.-](\d{1,2})[/.-](\d{4}|\d{2})|(\d{4})[/.-](\d{1,2})[/.-](\d{1,2}))$"
)


def data_valida(data: str) -> bool:
    # Primeiro filtro: a string precisa ter o formato de data
    m = detectar_formato_data.match(data.strip())
    if not m:
        return False

    # Se o grupo 1 existe, casou a alternativa dia/mês/ano; senão, casou ano/mês/dia
    if m.group(1):
        dia, mes, ano = m.group(1), m.group(2), m.group(3)
    else:
        ano, mes, dia = m.group(4), m.group(5), m.group(6)

    # Ano de 4 dígitos: só uma interpretação possível.
    # Ano de 2 dígitos (ex: "45"): pode ser 1945 ou 2045, então testa os dois séculos.
    # Isso evita deixar vazar a data de quem nasceu antes de 1969.
    anos = (int(ano),) if len(ano) == 4 else (1900 + int(ano), 2000 + int(ano))

    hoje = date.today()
    for a in anos:
        try:
            # date() lança ValueError se o dia/mês não existir (ex: 30/02, 29/02/2001)
            dt = date(a, int(mes), int(dia))
        except ValueError:
            continue  # essa interpretação do ano não forma data real; tenta a próxima

        # Data de nascimento plausível: não pode ser futura nem ter mais de 120 anos
        if date(hoje.year - 120, 1, 1) <= dt <= hoje:
            return True  # basta uma interpretação válida para aceitar

    return False

def detectar_datas_nascimento(texto: str) -> list[Ocorrencia]:
    return coletar_ocorrencias(detectar_formato_data(texto), data_valida, grupo=1)