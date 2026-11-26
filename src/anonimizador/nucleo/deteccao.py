import re
from collections.abc import Callable, Iterable

# Alias de tipo: uma ocorrência é (valor encontrado, posição inicial, posição final)
Ocorrencia = tuple[str, int, int]


def coletar_ocorrencias(
    matches: Iterable[re.Match[str]],  # resultados do re.finditer de cada detector
    validar: Callable[[str], bool]
    | None = None,  # função de validação (ex: cpf_valido); None = sem validação
    grupo: int = 0,  # 0 = match inteiro; 1 = primeiro grupo de captura
) -> list[Ocorrencia]:
    # set: se duas regras acharem o mesmo trecho na mesma posição, ele entra uma vez só
    achados: set[Ocorrencia] = set()

    for m in matches:
        # Pega o texto do grupo escolhido.
        # Nos padrões com lookahead ou captura, é o grupo 1.
        valor = m.group(grupo)

        # Sem validador, aceita tudo (caso do e-mail).
        # Com validador, só aceita se passar.
        if validar is None or validar(valor):
            # m.span(grupo) devolve (inicio, fim); o * desempacota os dois na tupla
            achados.add((valor, *m.span(grupo)))

    # Ordena pela posição inicial para o resultado seguir a ordem do texto
    return sorted(achados, key=lambda o: o[1])
