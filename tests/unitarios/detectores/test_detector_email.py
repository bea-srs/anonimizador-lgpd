import pytest
from src.anonimizador.detectores.detector_email import detectar_emails


def valores(resultado):
    return [valor for valor, _, _ in resultado]


# --- detecção de formatos válidos ---

@pytest.mark.parametrize(
    "texto, esperado",
    [
        ("ana@exemplo.com", "ana@exemplo.com"),
        ("ana.silva@empresa.com.br", "ana.silva@empresa.com.br"),
        ("user+lgpd@dominio.org", "user+lgpd@dominio.org"),
        ("contato_123@sub.dominio-teste.net", "contato_123@sub.dominio-teste.net"),
    ],
)
def test_detecta_emails_validos(texto, esperado):
    resultado = detectar_emails(texto)
    assert len(resultado) == 1
    assert resultado[0][0] == esperado


@pytest.mark.parametrize(
    "texto, esperado",
    [
        ("E-mail: ana@exemplo.com.", "ana@exemplo.com"),
        ("Enviar para (ana@exemplo.com), ok?", "ana@exemplo.com"),
        ("Linha 1\nana@exemplo.com\nLinha 2", "ana@exemplo.com"),
    ],
)
def test_detecta_email_com_pontuacao_ou_quebra_de_linha(texto, esperado):
    resultado = detectar_emails(texto)
    assert len(resultado) == 1
    assert resultado[0][0] == esperado


# --- posições, deduplicação e ordem ---

def test_posicoes_apontam_para_o_trecho_correto():
    texto = "Contato principal: ana@exemplo.com, secundário: suporte@empresa.com.br."
    resultado = detectar_emails(texto)
    assert len(resultado) == 2
    for valor, inicio, fim in resultado:
        assert texto[inicio:fim] == valor


def test_mesmo_email_em_posicoes_diferentes_sai_duas_vezes():
    texto = "Copie ana@exemplo.com e também ana@exemplo.com"
    resultado = detectar_emails(texto)
    assert len(resultado) == 2
    assert valores(resultado) == ["ana@exemplo.com", "ana@exemplo.com"]
    assert resultado[0][1] < resultado[1][1]


def test_emails_diferentes_em_ordem_de_posicao():
    texto = "Segundo: b@teste.com | Primeiro: a@teste.com"
    resultado = detectar_emails(texto)
    assert valores(resultado) == ["b@teste.com", "a@teste.com"]


# --- texto vazio, sem e-mail e falsos positivos ---

def test_texto_vazio():
    assert detectar_emails("") == []


@pytest.mark.parametrize(
    "texto",
    [
        "Olá, tudo bem? Pedido número 1234.",
        "01310-100",
        "+55 (11) 91234-5678",
        "529.982.247-25",
        "usuario@dominio",        # sem TLD
        "usuario@.com",           # domínio vazio
        "@exemplo.com",           # usuário vazio
        "usuario@exemplo.c",      # TLD com menos de 2 letras
    ],
)
def test_nao_detecta_textos_sem_email_valido(texto):
    assert detectar_emails(texto) == []