import pytest

from src.anonimizador.detectores.detector_cep import (
    cep_valido,
    detectar_ceps,
)
from src.anonimizador.nucleo.utils import extrair_digitos


def valores(resultado):
    return [valor for valor, _, _ in resultado]


# --- cep_valido ---

@pytest.mark.parametrize("cep", ["01310-100", "01310100"])
def test_cep_valido(cep):
    assert cep_valido(cep) is True


@pytest.mark.parametrize("cep", ["00000-000", "11111111", "01310-10", "013101000", ""])
def test_cep_invalido(cep):
    assert cep_valido(cep) is False


# --- regra 1: formato ---

def test_formato_com_hifen():
    assert detectar_ceps("01310-100") == [("01310-100", 0, 9)]


@pytest.mark.parametrize("texto", ["013101000", "01310-10", "001310-1000"])
def test_formato_incorreto_nao_e_cep(texto):
    assert detectar_ceps(texto) == []


# --- regra 2: palavra ---

@pytest.mark.parametrize("texto", [
    "CEP: 01310100",
    "cep: 01310-100",
    "Cep:01310100",
    "zip: 01310100",
    "zip code: 01310100",
    "zipcode 01310100",
    "código postal 01310-100",
    "codigo postal: 01310100",
    "CEP-01310100",
])
def test_palavra_chave_detecta(texto):
    resultado = detectar_ceps(texto)
    assert len(resultado) == 1
    assert extrair_digitos(resultado[0][0]) == "01310100"


def test_palavra_com_quebra_de_linha():
    assert detectar_ceps("CEP:\n01310100") == [("01310100", 5, 13)]


@pytest.mark.parametrize("texto", [
    "cepa:01310100",                  # \b impede "cepa"
    "o cep da loja é desconhecido",   # palavra sem número
    "CEP 123456789",                  # 9 dígitos
    "CEP: 00000000",                  # dígitos repetidos
])
def test_palavra_chave_nao_detecta(texto):
    assert detectar_ceps(texto) == []


# ---  testes de borda (bordas [\d.-] e janela \W{0,5}) ---

@pytest.mark.parametrize("texto", [
    "99-01310-100",                   # prefixo com hífen colado
    "01310-100-99",                   # sufixo com hífen colado
    "12.01310-100",                   # prefixo com ponto colado
    "01310-100.45",                   # sufixo com ponto colado
    "CEP: 99-01310100",               # prefixo colado mesmo após palavra-chave
])
def test_bordas_com_hifen_ou_ponto_nao_detectam(texto):
    assert detectar_ceps(texto) == []


@pytest.mark.parametrize("texto", [
    "CEP:   01310100",                # 5 caracteres não-palavra (":   ") dentro do \W{0,5}
    "CEP - 01310100",                 # 3 caracteres (" - ") dentro do \W{0,5}
])
def test_palavra_chave_dentro_do_limite_detecta(texto):
    resultado = detectar_ceps(texto)
    assert len(resultado) == 1
    assert extrair_digitos(resultado[0][0]) == "01310100"


@pytest.mark.parametrize("texto", [
    "CEP:     01310100",              # 7 caracteres não-palavra excede \W{0,5}
    "CEP (entrega): 01310100",        # letras no meio excedem \W{0,5}
])
def test_palavra_chave_fora_do_limite_nao_detecta(texto):
    assert detectar_ceps(texto) == []


# --- alternância, deduplicação e posição ---

def test_casa_nas_duas_regras_sai_uma_vez():
    assert detectar_ceps("CEP: 01310-100") == [("01310-100", 5, 14)]


def test_mesmo_cep_em_posicoes_diferentes_sai_duas_vezes():
    # as duas ocorrências precisam ser mascaradas
    resultado = detectar_ceps("CEP: 01310-100 e 01310-100")
    assert resultado == [("01310-100", 5, 14), ("01310-100", 17, 26)]


def test_ceps_diferentes_em_ordem_de_posicao():
    resultado = detectar_ceps("Entregar em 04538-132 ou em 01310-100")
    assert valores(resultado) == ["04538-132", "01310-100"]


def test_posicoes_apontam_para_o_trecho_correto():
    texto = "Cliente mora no CEP: 01310-100, filial em 04538-132."
    resultado = detectar_ceps(texto)
    assert len(resultado) == 2
    for valor, inicio, fim in resultado:
        assert texto[inicio:fim] == valor


def test_limitacao_cep_solto_sem_hifen_nao_e_detectado():
    # sem hífen e sem palavra-chave próxima, não detecta
    assert valores(detectar_ceps("CEP 01310-100 e 01310100")) == ["01310-100"]


# --- texto vazio / sem CEP ---

def test_texto_vazio():
    assert detectar_ceps("") == []


def test_texto_sem_cep():
    assert detectar_ceps("Olá, tudo bem? Pedido número 1234.") == []


# --- falsos positivos de outros detectores ---

@pytest.mark.parametrize("texto", ["+55 (11) 91234-5678", "529.982.247-25"])
def test_telefone_e_cpf_nao_sao_cep(texto):
    assert detectar_ceps(texto) == []