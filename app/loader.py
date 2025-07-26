import os
import fitz  # corretto: PyMuPDF è fitz, assicurarsi che pymupdf sia installato
from sentence_transformers import SentenceTransformer
import faiss
import pickle

EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")


def load_pdfs_and_index(commessa_id, pdf_dir="data/pdfs", db_dir="data/db"):
    pdf_chunks = []
    file_list = [f for f in os.listdir(pdf_dir) if f.startswith(str(commessa_id)) and f.endswith(".pdf")]

    for file in file_list:
        doc = fitz.open(os.path.join(pdf_dir, file))
        for page in doc:
            text = page.get_text()
            if len(text.strip()) > 20:
                pdf_chunks.append(text.strip())

    if not pdf_chunks:
        return None

    embeddings = EMBED_MODEL.encode(pdf_chunks)
    index = faiss.IndexFlatL2(embeddings[0].shape[0])
    index.add(embeddings)

    os.makedirs(db_dir, exist_ok=True)
    faiss.write_index(index, os.path.join(db_dir, f"{commessa_id}.index"))

    with open(os.path.join(db_dir, f"{commessa_id}_chunks.pkl"), "wb") as f:
        pickle.dump(pdf_chunks, f)

    return len(pdf_chunks)


