from detector_numero_tel import detectar_telefones
def test_telefone_com_pontuacao_e_ddi():
    assert detectar_telefones("+55 (11) 91234-5678") == ["+55 (11) 91234-5678"]

def test_telefone_so_digitos_sem_ddi():
    assert detectar_telefones("21912345678") == ["21912345678"]

def test_telefone_so_digitos_com_ddi():
    assert detectar_telefones("5581967225502") == ["5581967225502"]

def test_digitos_repetidos():
    assert detectar_telefones("99999999999") == []

def test_telefone_celular_invalido():
    assert detectar_telefones("218123456789") == []

def test_telefone_fixo_invalido():
    assert detectar_telefones("556696687323") == []

def test_telefone_sem_codigo_do_pais():
    assert detectar_telefones("1234567890") == ["1234567890"]

def test_telefone_sem_ddd():
    assert detectar_telefones("988646148") == []

def test_codigo_pais_com_mais_sem_espaco():
    assert detectar_telefones("+55(11) 97112-8594") == ["+55(11) 97112-8594"]

def test_codigo_pais_sem_mais():
    assert detectar_telefones("5511984321546") == ["5511984321546"]

def test_dentro_de_um_texto():
    texto = "Meus contatos são o 5511984321546 e o +55(11) 97112-8594, mas não liga pro (11) 89090-00560 não, que esse aí está desativado."
    esperado = ["5511984321546", "+55(11) 97112-8594"]
    assert detectar_telefones(texto) == esperado