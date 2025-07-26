from app.loader import load_pdfs_and_index
from app.search import cerca_risposta
from app.utils import estrai_commessa

if __name__ == "__main__":
    domanda = input("Inserisci la tua domanda: ")
    commessa = estrai_commessa(domanda)
    if not commessa:
        print("Errore: specificare 'commessa <numero>' nella domanda.")
    else:
        risposta = cerca_risposta(domanda, commessa)
        print("Risposta:
", risposta)
