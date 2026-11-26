import pytest

from src.anonimizador.detectores.detector_cpf import cpf_valido, detectar_cpfs
from src.anonimizador.nucleo.utils import extrair_digitos, todos_digitos_iguais


def valores(resultado):
    return [valor for valor, _, _ in resultado]


# --- helpers de utils ---


@pytest.mark.parametrize("sequencia", ["00000000000", "11111111111", "99999999"])
def test_todos_digitos_iguais_verdadeiro(sequencia):
    assert todos_digitos_iguais(sequencia) is True


@pytest.mark.parametrize("sequencia", ["03393226088", "11111111112", ""])
def test_todos_digitos_iguais_falso(sequencia):
    assert todos_digitos_iguais(sequencia) is False


# --- cpf_valido ---


@pytest.mark.parametrize(
    "cpf",
    [
        "033.932.260-88",
        "03393226088",
        "529.982.247-25",
        "52998224725",
    ],
)
def test_cpf_valido(cpf):
    assert cpf_valido(cpf) is True


@pytest.mark.parametrize(
    "cpf",
    [
        "000.000.000-00",
        "11111111111",
        "111.111.111.-88",  # Sequência repetida com pontuação estranha
        "033.932.260-89",  # segundo dígito verificador inválido
        "033.932.260-78",  # primeiro dígito verificador inválido
        "033.932.260-8",  # dígitos insuficientes
        "033.932.260-880",  # dígitos excedentes
        "",
    ],
)
def test_cpf_invalido(cpf):
    assert cpf_valido(cpf) is False


# --- formatos e casos colados ---


def test_cpf_colado_apos_prefixo_com_hifen():
    texto = "ID99-033.932.260-88"
    resultado = detectar_cpfs(texto)
    assert resultado == [("033.932.260-88", 5, 19)]
    assert texto[5:19] == "033.932.260-88"


@pytest.mark.parametrize(
    "texto, esperado",
    [
        ("033.932.260-88", "033.932.260-88"),
        ("03393226088", "03393226088"),
        ("CPF: 033.932.260-88.", "033.932.260-88"),
        ("User_03393226088;ok", "03393226088"),
        ("Ref#033.932.260-88/fim", "033.932.260-88"),
    ],
)
def test_detecta_formatos_validos(texto, esperado):
    resultado = detectar_cpfs(texto)
    assert len(resultado) == 1
    assert resultado[0][0] == esperado
    assert extrair_digitos(resultado[0][0]) == "03393226088"


@pytest.mark.parametrize(
    "texto",
    [
        "033932260889",  # 12 dígitos sem pontuação (bloqueado por (?!\d))
        "ID99-033.932.260-89",  # dígitos verificadores inválidos
        "111.111.111-11",  # todos os dígitos iguais
    ],
)
def test_nao_detecta_cpf_invalido_ou_excedente(texto):
    assert detectar_cpfs(texto) == []


# --- posições, deduplicação e ordem ---


def test_posicoes_apontam_para_o_trecho_correto():
    texto = "Cadastro ID99-033.932.260-88 e segundo 529.982.247-25."
    resultado = detectar_cpfs(texto)
    assert len(resultado) == 2
    for valor, inicio, fim in resultado:
        assert texto[inicio:fim] == valor


def test_mesmo_cpf_em_posicoes_diferentes_sai_duas_vezes():
    texto = "Primeiro ID99-033.932.260-88 e depois 033.932.260-88"
    resultado = detectar_cpfs(texto)
    assert len(resultado) == 2
    assert valores(resultado) == ["033.932.260-88", "033.932.260-88"]
    assert resultado[0][1] < resultado[1][1]


def test_cpfs_em_ordem_de_posicao():
    texto = "A: 529.982.247-25 | B: 033.932.260-88"
    resultado = detectar_cpfs(texto)
    assert valores(resultado) == ["529.982.247-25", "033.932.260-88"]


# --- texto vazio, sem CPF e falsos positivos ---


def test_texto_vazio():
    assert detectar_cpfs("") == []


@pytest.mark.parametrize(
    "texto",
    [
        "Olá, tudo bem? Pedido número 1234.",
        "01310-100",
        "+55 (11) 91234-5678",
        "ana@exemplo.com",
    ],
)
def test_nao_detecta_outros_dados_ou_texto_comum(texto):
    assert detectar_cpfs(texto) == []
