from faker import Faker
import csv
import random

def variar_formato(valor):
    if random.choice([True, False]):
        return valor  # Mantém com pontos e traços
    # Remove pontos, traços e barras
    return valor.replace(".", "").replace("-", "").replace("/", "")


from faker import Faker

def gerar_texto():
    fake = Faker("pt_BR")  # Geração de dados em formato brasileiro
    
    with open("data/texto_exemplo.txt", "w", encoding="utf-8") as arquivo:
        # Escreve o título uma única vez no início
        arquivo.write("Relatório de Cadastro de Usuários:\n\n")
        
        for f in range(100):
            frase = (
                f"O cliente {fake.name()}, portador do CPF {fake.cpf()}, "
                f"solicitou alteração cadastral. O e-mail principal para contato é "
                f"{fake.safe_email()} e o seu telefone de atendimento é {fake.phone_number()}.\n"
            )
            # Escreve cada frase no arquivo durante o loop
            arquivo.write(frase)


def gerar_csv():
    fake = Faker("pt_BR")
    with open("data/clientes_exemplo.csv", "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["Nome", "CPF", "E-mail", "Telefone", "CEP", "CNPJ", "RG"])   # cabeçalho, 1 vez, fora do for
        for _ in range(40):
            escritor.writerow([
                fake.name(), 
                variar_formato(fake.cpf()), 
                fake.email(), 
                fake.phone_number(), 
                variar_formato(fake.postcode()), 
                variar_formato(fake.cnpj()), 
                variar_formato(fake.rg())
            ])


if __name__ == "__main__":
    gerar_texto()
    gerar_csv()