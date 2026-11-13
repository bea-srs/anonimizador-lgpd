from detector_cpf import cpf_valido, detectar_cpfs

def test_cpf_valido_com_pontuacao():
  assert cpf_valido("529.982.247-25") is True

def test_cpf_valido_sem_pontuacao():
  assert cpf_valido("52998224725") is True

def test_cpf_com_digito_errado():
  assert cpf_valido("529.982.247-26") is False

def test_cpf_com_todos_digitos_iguais():
  assert cpf_valido("111.111.111-11") is False

def test_detectar_ignora_cpf_invalido():
  texto = "Meu CPF é 529.982.247-25 e o pedido é 123.456.789-00."
  assert detectar_cpfs(texto) == ['529.982.247-25']

def test_texto_vazio():
    assert detectar_cpfs("") == []

def test_texto_sem_cpf():
    assert detectar_cpfs("Olá, tudo bem? Pedido número 1234.") == []

def test_cpf_no_inicio_e_no_fim_do_texto():
    texto = "529.982.247-25 é o primeiro e o último é 991.690.460-00"
    assert detectar_cpfs(texto) == ["529.982.247-25", "991.690.460-00"]

def test_numero_grande_nao_e_cpf():
    # 14 dígitos: contém 11 dígitos, mas não é um CPF
    assert detectar_cpfs("código 52998224725123") == []

def test_cpf_com_menos_digitos():
    assert cpf_valido("529.982.247-2") is False

def test_cpf_com_letras():
    assert cpf_valido("abc.def.ghi-jk") is False