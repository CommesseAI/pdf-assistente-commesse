import streamlit as st
from app.utils import estrai_commessa
from app.search import cerca_risposta
from app.loader import load_pdfs_and_index

st.set_page_config(page_title="Assistente PDF Commesse", layout="wide")

# Header con logo e nome assistente
st.markdown("""
    <div style="display: flex; align-items: center; gap: 1rem;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Document_icon_-_noun_project_28230.svg/512px-Document_icon_-_noun_project_28230.svg.png" width="60">
        <h1 style="margin: 0;">Assistente Commesse AI</h1>
    </div>
    <hr>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("🔧 Indicizzazione PDF")
    commessa_input = st.text_input("ID Commessa da indicizzare")
    indicizza = st.button("Indicizza PDF")
    if indicizza and commessa_input:
        num = load_pdfs_and_index(commessa_input)
        if num:
            st.success(f"Indicizzati {num} blocchi di testo dalla commessa {commessa_input}")
        else:
            st.warning("Nessun PDF trovato o contenuto vuoto.")

st.markdown("Scrivi la tua domanda nel campo qui sotto. Ricorda di includere il numero di commessa.")

domanda = st.text_area("❓ Domanda", placeholder="Esempio: commessa 25154, posizione 5, che profilo è stato utilizzato?")
if st.button("Cerca risposta") and domanda:
    commessa_id = estrai_commessa(domanda)
    if commessa_id:
        risposta = cerca_risposta(domanda, commessa_id)
        st.markdown("### 🧠 Risposta")
        st.write(risposta)
    else:
        st.warning("Per favore includi 'commessa <numero>' nella domanda.")


