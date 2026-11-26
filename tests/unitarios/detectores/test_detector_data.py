from datetime import date, timedelta

import pytest

from anonimizador.detectores.detector_data import (
    data_valida,
    detectar_datas_nascimento,
)
from anonimizador.nucleo.utils import extrair_digitos


def valores(resultado):
    return [valor for valor, _, _ in resultado]


# --- data_valida ---


@pytest.mark.parametrize(
    "data",
    [
        "15/05/1990",
        "15/05/90",
        "1990-05-15",
        "1990/05/15",
        "15-05-1990",
        "15.05.1990",
        "29/02/2000",  # ano bissexto válido
        "05/03/1998",  # sem zero à esquerda
    ],
)
def test_data_valida(data):
    assert data_valida(data) is True


@pytest.mark.parametrize(
    "data",
    [
        "30/02/2000",  # 30 de fevereiro não existe
        "29/02/2001",  # 2001 não é bissexto
        "32/01/1995",  # dia inexistente
        "15/13/1995",  # mês inexistente
        "00/05/1995",  # dia zero
        "15/00/1995",  # mês zero
        "",
        "abc",
    ],
)
def test_data_invalida_calendario(data):
    assert data_valida(data) is False


def test_data_futura_e_invalida():
    amanha = (date.today() + timedelta(days=1)).strftime("%d/%m/%Y")
    assert data_valida(amanha) is False


def test_data_antiga_demais_e_invalida():
    data_antiga = f"01/01/{date.today().year - 150}"
    assert data_valida(data_antiga) is False


# --- detecção de formatos e casos colados ---


@pytest.mark.parametrize(
    "texto, esperado",
    [
        ("Nascimento: 15/05/1990.", "15/05/1990"),
        ("Nasc:1990-05-15", "1990-05-15"),
        ("ID99-15/05/1990", "15/05/1990"),
        ("Data 15.05.90 ok", "15.05.90"),
        ("Linha 1\n15/05/1990\nLinha 2", "15/05/1990"),
    ],
)
def test_detecta_formatos_validos(texto, esperado):
    resultado = detectar_datas_nascimento(texto)
    assert len(resultado) == 1
    assert resultado[0][0] == esperado
    assert len(extrair_digitos(resultado[0][0])) in (6, 8)


@pytest.mark.parametrize(
    "texto",
    [
        "Data inválida: 30/02/2000",
        "Ano futuro: 2099-01-01",
        "Sem barra nem hífen: 15051990",
    ],
)
def test_nao_detecta_data_invalida_ou_sem_separador(texto):
    assert detectar_datas_nascimento(texto) == []


# --- posições, deduplicação e ordem ---


def test_posicoes_apontam_para_o_trecho_correto():
    texto = "Titular nascido em 15/05/1990 e dependente em 1995-10-20."
    resultado = detectar_datas_nascimento(texto)
    assert len(resultado) == 2
    for valor, inicio, fim in resultado:
        assert texto[inicio:fim] == valor


def test_mesma_data_em_posicoes_diferentes_sai_duas_vezes():
    texto = "Primeiro 15/05/1990 e depois 15/05/1990"
    resultado = detectar_datas_nascimento(texto)
    assert len(resultado) == 2
    assert valores(resultado) == ["15/05/1990", "15/05/1990"]
    assert resultado[0][1] < resultado[1][1]


def test_datas_em_ordem_de_posicao():
    texto = "Segunda: 20/08/1988 | Primeira: 10/01/1992"
    resultado = detectar_datas_nascimento(texto)
    assert valores(resultado) == ["20/08/1988", "10/01/1992"]


# --- texto vazio e falsos positivos de outros detectores ---


def test_texto_vazio():
    assert detectar_datas_nascimento("") == []


@pytest.mark.parametrize(
    "texto",
    [
        "Olá, tudo bem? Pedido número 1234.",
        "01310-100",
        "033.932.260-88",
        "+55 (11) 91234-5678",
        "ana@exemplo.com",
    ],
)
def test_nao_detecta_outros_dados_ou_texto_comum(texto):
    assert detectar_datas_nascimento(texto) == []
