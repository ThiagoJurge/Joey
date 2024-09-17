import re

def extrair_designacao(text):
    """Extrai números de 7 a 8 dígitos de um texto."""
    return re.findall(r"\b\d{7,8}\b", text)
