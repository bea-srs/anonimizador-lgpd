import json
from pathlib import Path


def _ler_texto_com_fallback(caminho: Path) -> str:
    # Tenta ler o arquivo testando codificações comuns antes de usar substituição
    for encoding in ("utf-8", "cp1252", "latin-1"):
        try:
            return caminho.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    # Último recurso: substitui bytes inválidos para evitar falha de leitura
    return caminho.read_text(encoding="utf-8", errors="replace")


def _ler_txt(caminho: Path) -> str:
    # Lê arquivos .txt como texto puro
    return _ler_texto_com_fallback(caminho)


def _ler_csv(caminho: Path) -> str:
    # Por enquanto só lê como texto; a camada tabular entra aqui depois
    return _ler_texto_com_fallback(caminho)


def _ler_json(caminho: Path) -> str:
    # Lê o conteúdo textual do JSON, valida a estrutura e formata de modo legível
    conteudo = _ler_texto_com_fallback(caminho)
    dados = json.loads(conteudo)
    return json.dumps(dados, ensure_ascii=False, indent=2)


def _ler_pdf(caminho: Path) -> str:
    # Importa pypdf apenas quando um PDF é lido.
    # Evita exigir a biblioteca para outros formatos.
    from pypdf import PdfReader

    # Abre o PDF e extrai o texto de cada página (usa "" se a página não tiver texto)
    leitor = PdfReader(caminho)
    paginas = [pagina.extract_text() or "" for pagina in leitor.pages]
    # Une o texto das páginas separando por linha em branco
    return "\n\n".join(paginas)


# Tabela de despacho que associa cada extensão suportada à sua função leitora
LEITORES = {
    ".txt": _ler_txt,
    ".csv": _ler_csv,
    ".json": _ler_json,
    ".pdf": _ler_pdf,
}


def ler_texto(caminho: str | Path) -> str:
    # Converte o caminho para Path e valida se o arquivo realmente existe
    caminho_path = Path(caminho)
    if not caminho_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_path}")

    # Normaliza a extensão para minúscula e verifica se há leitor registrado
    extensao = caminho_path.suffix.lower()
    if extensao not in LEITORES:
        raise ValueError(f"Extensão {extensao} não é suportada")

    # Executa a função correspondente à extensão e retorna o texto extraído
    return LEITORES[extensao](caminho_path)
