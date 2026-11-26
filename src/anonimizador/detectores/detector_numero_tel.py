import re


def extrair_digitos(texto):
    # Recebe '+55 (11) 91234-5678' e devolve '5511912345678'.
    return re.sub(r'[^0-9]', '', texto)


def remover_codigo_pais(digitos):
    # Se os dígitos começarem com 55 e sobrarem 12 ou 13, tira o 55. Senão, devolve como veio
    if digitos.startswith('55') and len(digitos) in (12, 13):
        return digitos[2:]
    else:
        return digitos


def telefone_valido(telefone):
    # Recebe um telefone (com ou sem pontuação) e devolve True ou False
    numero = extrair_digitos(telefone)
    numero = remover_codigo_pais(numero)

    if len(numero) not in (10,11):
      return False

    # ddd valido
    ddd = numero[:2]
    # Passando a string do padrão diretamente para o re.match para evitar o erro de unhashable list
    if not re.match(r"^(1[1-9]|2[12478]|3[1-578]|4[1-9]|5[13-5]|6[1-9]|7[13-579]|8[1-9]|9[1-9])$", ddd):
      return False
    
    # se tem 11 dígitos, o numero[2] deve ser "9"
    if len(numero) == 11 and numero[2] != '9':
      return False

    # se tem 10 dígitos, o numero[2] deve estar entre "2" e "5"
    if len(numero) == 10 and numero[2] not in '2345':
      return False

    # Rejeita se todos os dígitos forem iguais ou se for uma sequência óbvia
    if len(set(numero)) == 1 or numero in (
        "12345678901",
        "01234567890",
        "98765432109",
    ):
        return False
        
    return True


def detectar_telefones(texto):
    # Recebe um texto e devolve a lista de telefones VÁLIDOS encontrados nele.

    numero_telefone = re.findall(r"(?<!\d)(?:\+?55\s?)?\(?\d{2}\)?\s?\d{4,5}[\s-]?\d{4}(?!\d)", texto)
    return [t for t in numero_telefone if telefone_valido(t)]