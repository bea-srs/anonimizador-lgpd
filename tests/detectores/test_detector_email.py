from detector_email import detectar_emails

def test_padrao():
  texto = "Envie um e-mail para antidio27@gmail.com"
  esperado = ["antidio27@gmail.com"]
  assert detectar_emails(texto) == esperado

def test_sem_tld():
  assert detectar_emails("odeta6988@example") == []

def test_com_subdominio():
  texto = "Por favor, envie os relatórios atualizados para o e-mail de rosimar178@example.com.br até o final da tarde."
  esperado = ["rosimar178@example.com.br"]
  assert detectar_emails(texto) == esperado

def test_com_dois_arroba():
  assert detectar_emails("antidio27@@example.com") == []

def test_com_caracteres_especiais_invalido():
  assert detectar_emails("Ossyes!@example.com") == []

def test_com_caracteres_especiais_valido():
  assert detectar_emails("Ossyes_@example.com") == ["Ossyes_@example.com"]

def test_sem_email():
  texto = "Acesse o site praPrika.com"
  esperado = []
  assert detectar_emails(texto) == esperado

def test_texto_vazio():
  assert detectar_emails("") == []

def test_dois_emails():
  texto= "Por favor, envie a proposta de contato@empresaexample.com para joao.silva@example.com.br assim que possível."
  esperado = ["contato@empresaexample.com","joao.silva@example.com.br"]
  assert detectar_emails(texto) == esperado