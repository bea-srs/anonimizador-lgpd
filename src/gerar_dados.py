from faker import Faker
import csv

def gerar_texto():
    fake = Faker("pt_BR") #geração de dados em formato brasileiro
    with open("data/texto_exemplo.txt", "w", encoding="utf-8") as arquivo:
        titulo = "\n Relatório de Cadastro de Usuários:\n"
        for f in range(100):
            frase = f"\nO cliente {fake.name()}, portador do CPF {fake.cpf()}, solicitou alteração cadastral. O e-email principal para contato é {fake.safe_email()} e o seu telefone de atendimento é {fake.phone_number()}\n"

        arquivo.write(f"{titulo}{frase}")
        return


def gerar_csv():
    fake = Faker("pt_BR")
    with open("data/clientes_exemplo.csv", "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["nome", "cpf", "email", "telefone"])   # cabeçalho, 1 vez, fora do for
        for _ in range(20):
            escritor.writerow([fake.name(), fake.cpf(), fake.email(), fake.phone_number()])



if __name__ == "__main__":
    gerar_texto()
    gerar_csv()