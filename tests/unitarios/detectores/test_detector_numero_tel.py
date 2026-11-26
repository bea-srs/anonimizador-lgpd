import pytest

from src.anonimizador.detectores.detector_numero_tel import (
    detectar_telefones,
    remover_codigo_pais,
    telefone_valido,
)
from src.anonimizador.nucleo.utils import extrair_digitos


def valores(resultado):
    return [valor for valor, _, _ in resultado]


# --- remover_codigo_pais ---

@pytest.mark.parametrize(
    "digitos, esperado",
    [
        ("5511912345678", "11912345678"),   # celular com DDI 55 (13 dígitos)
        ("551133445566", "1133445566"),     # fixo com DDI 55 (12 dígitos)
        ("5533445566", "5533445566"),       # DDD 55 (Santa Maria/RS) com 10 dígitos -> mantém 55
        ("11912345678", "11912345678"),     # sem DDI (11 dígitos)
        ("1133445566", "1133445566"),       # sem DDI (10 dígitos)
    ],
)
def test_remover_codigo_pais(digitos, esperado):
    assert remover_codigo_pais(digitos) == esperado


# --- telefone_valido ---

@pytest.mark.parametrize(
    "telefone",
    [
        "+55 (11) 91234-5678",
        "55 11 91234-5678",
        "(21) 98765-4321",
        "11912345678",
        "(11) 3344-5566",
        "2125401234",
        "(55) 3220-1234",       # DDD 55 válido + fixo começando com 3
    ],
)
def test_telefone_valido(telefone):
    assert telefone_valido(telefone) is True


@pytest.mark.parametrize(
    "telefone",
    [
        "(00) 91234-5678",      # DDD inexistente
        "(10) 91234-5678",      # DDD inexistente
        "(11) 81234-5678",      # 11 dígitos sem 9 na frente
        "(11) 1234-5678",       # 10 dígitos começando com 1
        "(11) 9234-5678",       # 10 dígitos começando com 9
        "(11) 9123-5678",       # só 8 dígitos após DDD (9 no total)
        "(11) 91234-56789",     # dígitos a mais
        "11111111111",          # dígitos repetidos
        "12345678901",          # sequência óbvia
        "01234567890",          # sequência óbvia
        "98765432109",          # sequência óbvia
        "",
    ],
)
def test_telefone_invalido(telefone):
    assert telefone_valido(telefone) is False


# --- detecção de formatos ---

@pytest.mark.parametrize(
    "texto, esperado",
    [
        ("Celular: +55 (11) 91234-5678.", "+55 (11) 91234-5678"),
        ("Fixo (11) 3344-5566 no escritório", "(11) 3344-5566"),
        ("Tel: 11912345678", "11912345678"),
        ("ID99-(21) 98765-4321", "(21) 98765-4321"),
        ("Contato 11-91234-5678 ok", "11-91234-5678"),
    ],
)
def test_detecta_formatos_validos(texto, esperado):
    resultado = detectar_telefones(texto)
    assert len(resultado) == 1
    assert resultado[0][0] == esperado
    assert len(extrair_digitos(resultado[0][0])) in (10, 11, 12, 13)


@pytest.mark.parametrize(
    "texto",
    [
        "119123456789",         # 12 dígitos sem DDI (bloqueado por (?!\d))
        "(11) 81234-5678",      # celular sem dígito 9
        "(11) 1234-5678",       # fixo inválido começando com 1
        "(99) 11111-1111",      # todos os dígitos iguais
        "12345678901",          # sequência óbvia
    ],
)
def test_nao_detecta_telefone_invalido_ou_excedente(texto):
    assert detectar_telefones(texto) == []


# --- posições, deduplicação e ordem ---

def test_posicoes_apontam_para_o_trecho_correto():
    texto = "Ligar para +55 (11) 91234-5678 ou para (21) 3344-5566."
    resultado = detectar_telefones(texto)
    assert len(resultado) == 2
    for valor, inicio, fim in resultado:
        assert texto[inicio:fim] == valor


def test_mesmo_telefone_em_posicoes_diferentes_sai_duas_vezes():
    texto = "Primeiro (11) 91234-5678 e depois (11) 91234-5678"
    resultado = detectar_telefones(texto)
    assert len(resultado) == 2
    assert valores(resultado) == ["(11) 91234-5678", "(11) 91234-5678"]
    assert resultado[0][1] < resultado[1][1]


def test_telefones_em_ordem_de_posicao():
    texto = "Segundo: (21) 98765-4321 | Primeiro: (11) 91234-5678"
    resultado = detectar_telefones(texto)
    assert valores(resultado) == ["(21) 98765-4321", "(11) 91234-5678"]


# --- texto vazio, sem telefone e falsos positivos ---

def test_texto_vazio():
    assert detectar_telefones("") == []


@pytest.mark.parametrize(
    "texto",
    [
        "Olá, tudo bem? Pedido número 1234.",
        "01310-100",
        "033.932.260-88",
        "ana@exemplo.com",
    ],
)
def test_nao_detecta_outros_dados_ou_texto_comum(texto):
    assert detectar_telefones(texto) == []