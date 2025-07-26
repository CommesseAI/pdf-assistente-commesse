import os
import faiss
import pickle
from sentence_transformers import SentenceTransformer
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import streamlit as st

EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")


def carica_index(commessa_id, db_dir="data/db"):
    index_path = os.path.join(db_dir, f"{commessa_id}.index")
    chunks_path = os.path.join(db_dir, f"{commessa_id}_chunks.pkl")

    if not os.path.exists(index_path) or not os.path.exists(chunks_path):
        return None, None

    index = faiss.read_index(index_path)
    with open(chunks_path, "rb") as f:
        chunks = pickle.load(f)

    return index, chunks


def cerca_risposta(domanda, commessa_id, top_k=5):
    index, chunks = carica_index(commessa_id)
    if index is None:
        return "Nessun indice trovato per la commessa specificata."

    query_vec = EMBED_MODEL.encode([domanda])
    D, I = index.search(query_vec, top_k)
    contesto = "
".join([chunks[i] for i in I[0] if i < len(chunks)])

    prompt = f"""
Rispondi alla seguente domanda usando solo le informazioni nel contesto fornito.

Contesto:
{contesto}

Domanda: {domanda}
Risposta:
"""

    try:
        risposta = llm([HumanMessage(content=prompt)]).content
        return risposta
    except Exception as e:
        st.error("Errore nella generazione della risposta. Verifica la tua API key OpenAI.")
        return str(e)


