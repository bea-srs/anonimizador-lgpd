import csv
import random
import re
from pathlib import Path

from faker import Faker


def sortear_campos(fake: Faker, rng: random.Random) -> dict[str, str]:
    # Sorteia o formato da data e já aplica a formatação no nascimento
    formato_data = rng.choice(["%d/%m/%Y", "%d/%m/%y", "%Y-%m-%d"])
    data_nascimento = fake.date_of_birth().strftime(formato_data)

    # Alterna entre CPF formatado e apenas dígitos
    cpf_base = fake.cpf()
    cpf = cpf_base if rng.choice([True, False]) else re.sub(r"\D", "", cpf_base)

    # Alterna entre CEP com hífen e sem hífen
    cep_base = fake.postcode()
    cep = cep_base if rng.choice([True, False]) else cep_base.replace("-", "")

    # Varia o telefone: mantém/limpa pontuação ou deixa só dígitos (com ou sem DDI 55)
    tel_base = fake.phone_number()
    if rng.choice([True, False]):
        # Mantém como veio ou remove apenas traços e parênteses
        telefone = (
            tel_base
            if rng.choice([True, False])
            else re.sub(r"[()-]", "", tel_base).strip()
        )
    else:
        # Extrai só dígitos e remove o prefixo 55 quando houver DDI + DDD + número
        digitos = re.sub(r"\D", "", tel_base)
        if digitos.startswith("55") and len(digitos) > 11 and rng.choice([True, False]):
            digitos = digitos[2:]
        telefone = digitos

    # Retorna um registro completo com os campos prontos para texto ou CSV
    return {
        "nome": fake.name(),
        "cpf": cpf,
        "data_nascimento": data_nascimento,
        "email": fake.safe_email(),
        "telefone": telefone,
        "cep": cep,
    }


def gerar_texto(
    fake: Faker, rng: random.Random, destino: Path, quantidade: int = 25
) -> None:
    # Inicia o documento com título e acumula os parágrafos gerados
    linhas = ["Relatório de Cadastro de Usuários:\n\n"]
    for _ in range(quantidade):
        dados = sortear_campos(fake, rng)
        frase = (
            f"Eu, {dados['nome']}, nascida em {dados['data_nascimento']}, "
            f"inscrita no CPF sob o nº {dados['cpf']}, "
            f"residente no endereço correspondente ao CEP {dados['cep']}, "
            f"declaro para os devidos fins que os dados informados"
            f"neste cadastro são verdadeiros.\n"
            f"Para eventuais contatos ou confirmações, disponibilizo o telefone "
            f"{dados['telefone']} e meu e-mail {dados['email']}.\n\n"
        )
        linhas.append(frase)

    # Grava o arquivo final em UTF-8
    destino.write_text("".join(linhas), encoding="utf-8")


def gerar_csv(
    fake: Faker, rng: random.Random, destino: Path, quantidade: int = 100
) -> None:
    # Define os nomes das colunas no padrão snake_case
    cabecalho = [
        "cliente_nome",
        "cliente_cpf",
        "data_nascimento",
        "endereco_email",
        "telefone_contato",
        "postal_code",
    ]
    # newline="" evita linhas em branco extras no csv.writer
    with destino.open("w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(cabecalho)
        for _ in range(quantidade):
            dados = sortear_campos(fake, rng)
            escritor.writerow(
                [
                    dados["nome"],
                    dados["cpf"],
                    dados["data_nascimento"],
                    dados["email"],
                    dados["telefone"],
                    dados["cep"],
                ]
            )


def main() -> None:
    pasta_saida = Path("data/exemplos")
    # Garante que a pasta de destino exista
    pasta_saida.mkdir(parents=True, exist_ok=True)

    # Geração de dados em formato brasileiro e gerador aleatório local
    fake = Faker("pt_BR")
    rng = random.Random()

    # Descomente para tornar a geração reproduzível:
    # seed = 42
    # fake.seed_instance(seed)
    # rng.seed(seed)

    # Gera os arquivos de exemplo em TXT e CSV
    gerar_texto(fake, rng, pasta_saida / "declaracao_exemplo.txt", quantidade=25)
    gerar_csv(fake, rng, pasta_saida / "clientes_exemplo.csv", quantidade=100)


if __name__ == "__main__":
    # Executa apenas quando o script é rodado diretamente
    main()
