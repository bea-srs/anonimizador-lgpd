import re


def extrair_digitos(texto):
    # Recebe um texto e devolve apenas os dígitos.
    return re.sub(r"\D", "", texto)



def cpf_valido(cpf):
    # Recebe um CPF (com ou sem pontuação) e devolve True ou False.
    numero = extrair_digitos(cpf)

    # verifica se tem 11 digitos ou se é uma sequencia de repetida (ex: 111.111.111.-88)
    if len(numero) != 11:
      return False
    if numero == numero[0] * 11:
      return False


    # calcula os digitos verificadores
    soma = sum(int(numero[i]) * (10 - i) for i in range(9))
    digito1 = (soma * 10) % 11
    if digito1 ==10:
      digito1 = 0
    if digito1 != int(numero[9]):
      return False

    soma = sum(int(numero[i])* (11 - i) for i in range(10))
    digito2 = (soma * 10) % 11
    if digito2 ==10:
      digito2 = 0
    if digito2 != int(numero[10]):
      return False

    return True


def detectar_cpfs(texto):
    # Recebe um texto e devolve a lista de CPFs VÁLIDOS encontrados nele.
    #print("texto recebido:", texto)
    pessoa_fisica = re.findall(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b", texto)
    # print("pessoa_fisica:", pessoa_fisica)
    return [c for c in pessoa_fisica if cpf_valido(c)] # retorna só os cpf válidos