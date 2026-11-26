import re

def detectar_emails(texto):
    # Recebe um texto e devolve a lista de e-mails encontrados 
    padrao = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    emails = re.findall(padrao, texto)
    return emails