import re
from datetime import date

from anonimizador.nucleo.deteccao import Ocorrencia, coletar_ocorrencias

# Compilado uma vez só (mais eficiente que recompilar a cada chamada)
# Alternativa 1: dia, mês e ano (15/05/1990 ou 15.05.90)
# Alternativa 2: ano, mês e dia (1990-05-15)


PADRAO_DATA = re.compile(
    r"("
    r"(\d{1,2})/(\d{1,2})/(\d{4}|\d{2})"
    r"|"
    r"(\d{1,2})\.(\d{1,2})\.(\d{4}|\d{2})"
    r"|"
    r"(\d{1,2})-(\d{1,2})-(\d{4}|\d{2})"
    r"|"
    r"(\d{4})-(\d{1,2})-(\d{1,2})"
    r"|"
    r"(\d{4})/(\d{1,2})/(\d{1,2})"
    r")"
)


def data_valida(data: str) -> bool:
    # Primeiro filtro: a string precisa ter o formato de data
    m = PADRAO_DATA.fullmatch(data.strip())
    if not m:
        return False

    # Identifica qual formato foi encontrado
    if m.group(2):
        dia, mes, ano = m.group(2), m.group(3), m.group(4)
    elif m.group(5):
        dia, mes, ano = m.group(5), m.group(6), m.group(7)
    elif m.group(8):
        dia, mes, ano = m.group(8), m.group(9), m.group(10)
    elif m.group(11):
        ano, mes, dia = m.group(11), m.group(12), m.group(13)
    else:
        ano, mes, dia = m.group(14), m.group(15), m.group(16)

    # Ano de 4 dígitos: uma interpretação.
    # Ano de 2 dígitos: testa os dois séculos.
    anos = (int(ano),) if len(ano) == 4 else (1900 + int(ano), 2000 + int(ano))

    hoje = date.today()

    for a in anos:
        try:
            dt = date(a, int(mes), int(dia))
        except ValueError:
            continue

        # Data não pode ser futura nem ter mais de 120 anos
        if date(hoje.year - 120, 1, 1) <= dt <= hoje:
            return True

    return False


def detectar_datas_nascimento(texto: str) -> list[Ocorrencia]:
    matches = PADRAO_DATA.finditer(texto)

    return coletar_ocorrencias(matches, data_valida, grupo=1)
