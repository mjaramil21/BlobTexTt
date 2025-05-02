import streamlit as st
import pandas as pd
from textblob import TextBlob
from googletrans import Translator
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re

# --- ESTILO DEL ORÁCULO ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=UnifrakturCook:wght@700&display=swap');

    html, body, [class*="css"]  {
        background-image: url('image_2025-05-02_125422352.png');
        background-size: cover;
        background-attachment: fixed;
        color: #f9f5e5;
        font-family: 'Georgia', serif;
    }

    h1, h2, h3 {
        font-family: 'UnifrakturCook', cursive;
        color: #e8d382;
        text-shadow: 2px 2px 4px #000000;
    }

    .stTextInput > div > div > input,
    .stTextArea > div > textarea {
        background-color: rgba(255, 255, 255, 0.1);
        color: #f9f5e5;
        border: 1px solid #c0a96e;
    }

    .stButton > button {
        background-color: #3b2d1f;
        color: #e8d382;
        border: none;
        border-radius: 5px;
        transition: 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #7a6a4f;
        color: white;
    }

    .sidebar .sidebar-content {
        background-color: rgba(0, 0, 0, 0.5);
    }

    .recuadro {
        background-color: rgba(30, 30, 30, 0.6);
        padding: 0.5em;
        margin-bottom: 0.5em;
        border-left: 5px solid #e8d382;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- TÍTULO Y DESCRIPCIÓN ---
st.markdown("<h1>🔮 El Oráculo de los Poetas 🔮</h1>", unsafe_allow_html=True)
st.markdown("*Ingresa un texto y permite que el oráculo revele los secretos escondidos entre tus palabras...*")

# --- ENTRADA DEL TEXTO ---
text = st.text_area("📝 Ofrece tu texto al oráculo:")

if text:
    words = re.findall(r'\w+', text.lower())
    word_freq = {w: words.count(w) for w in set(words)}

    st.markdown("## 🌌 Palabras Mágicas")
    st.markdown("*Estas son las palabras más poderosas que emergen de tu conjuro textual:*")

    wordcloud = WordCloud(width=800, height=400, background_color=None, mode='RGBA',
                          colormap='inferno').generate_from_frequencies(word_freq)

    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)

    st.markdown("## 📜 Profecía del Texto")
    num_words = len(words)
    num_sentences = len(re.findall(r'[.!?]+', text))
    unique_words = len(set(words))

    st.write(f"🔸 Número de palabras: **{num_words}**")
    st.write(f"🔸 Número de oraciones: **{num_sentences}**")
    st.write(f"🔸 Palabras únicas: **{unique_words}**")

    st.markdown("## 🧿 Runas Repetidas")
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
    for word, freq in sorted_words:
        st.write(f"🔹 **{word}** — {freq} veces")

# --- BARRA LATERAL ---
with st.sidebar:
    st.image("image_2025-05-02_125422352.png", use_container_width=True)
    st.title("⚙️ Opciones del ritual")
    modo = st.selectbox("Elige el método de invocación:", ["Texto directo", "Archivo de texto"])

# --- FUNCIONES ---
translator = Translator()

def traducir_texto(texto):
    try:
        return translator.translate(texto, src='es', dest='en').text
    except Exception as e:
        st.error(f"Error al traducir: {e}")
        return texto

def contar_palabras(texto):
    stop_words = set(["el", "la", "los", "las", "de", "y", "a", "en", "que", "es", "con", "por", "para", "una", "un"])
    palabras = re.findall(r'\b\w+\b', texto.lower())
    palabras_filtradas = [p for p in palabras if p not in stop_words and len(p) > 2]
    contador = {}
    for p in palabras_filtradas:
        contador[p] = contador.get(p, 0) +

