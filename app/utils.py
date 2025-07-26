import re

def estrai_commessa(domanda):
    match = re.search(r"commessa\s*(\d+)", domanda.lower())
    return match.group(1) if match else None


