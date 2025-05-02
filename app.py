import streamlit as st
import pandas as pd
from textblob import TextBlob
import re
from googletrans import Translator


st.set_page_config(
    page_title="El oráculo de los poetas",
    layout="wide"
)


st.markdown("""
    <style>
        body {
            background-color: #EDE8D0;
            color: (#8B4411;
        }
        .main {
            background-color: #EDE8D0 !important;
            color: #2B2B2B !important;
        }
        .stApp {
            font-family: 'Times New Roman';
        }
        .block-container {
            padding-top: 2rem;
        }
        h1, h2, h3, h4 {
            color: #2B2B2B;
        }
        .stProgress > div > div > div > div {
            background-color: #FFB085;
        }
        .recuadro {
            background-color: white;
            color: black;
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 1rem;
            box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
        }
        button[kind="primary"] {
            background-color: #FFD1BA !important;
            color: #2B2B2B !important;
            border: none !important;
        }
        .stButton>button {
            background-color: #FFD1BA;
            color: #2B2B2B;
            font-weight: bold;
            border-radius: 8px;
            padding: 0.5rem 1rem;
        }
    </style>
""", unsafe_allow_html=True)


with st.sidebar:
    st.image("owoawa.png", use_container_width=True)
    st.title("Opciones")
    modo = st.selectbox(
        "Selecciona el modo de entrada:",
        ["Texto directo", "Archivo de texto"]
    )

def contar_palabras(texto):
    stop_words = set([...])  
    palabras = re.findall(r'\b\w+\b', texto.lower())
    palabras_filtradas = [p for p in palabras if p not in stop_words and len(p) > 2]
    contador = {}
    for p in palabras_filtradas:
        contador[p] = contador.get(p, 0) + 1
    return dict(sorted(contador.items(), key=lambda x: x[1], reverse=True)), palabras_filtradas


translator = Translator()

def traducir_texto(texto):
    try:
        return translator.translate(texto, src='es', dest='en').text
    except Exception as e:
        st.error(f"Error al traducir: {e}")
        return texto


def procesar_texto(texto):
    texto_original = texto
    texto_ingles = traducir_texto(texto)
    blob = TextBlob(texto_ingles)
    sentimiento = blob.sentiment.polarity
    subjetividad = blob.sentiment.subjectivity
    frases_originales = [f.strip() for f in re.split(r'[.!?]+', texto_original) if f.strip()]
    frases_traducidas = [f.strip() for f in re.split(r'[.!?]+', texto_ingles) if f.strip()]
    frases_combinadas = [{"original": o, "traducido": t} for o, t in zip(frases_originales, frases_traducidas)]
    contador_palabras, palabras = contar_palabras(texto_ingles)
    return {
        "sentimiento": sentimiento,
        "subjetividad": subjetividad,
        "frases": frases_combinadas,
        "contador_palabras": contador_palabras,
        "palabras": palabras,
        "texto_original": texto_original,
        "texto_traducido": texto_ingles
    }


def crear_visualizaciones(resultados):
    col1, col2 = st.columns(2)
    with col1:
        with st.container():
            st.subheader("Análisis de Sentimiento")
            st.progress((resultados["sentimiento"] + 1) / 2)
            if resultados["sentimiento"] > 0.05:
                st.success(f"📈 Positivo ({resultados['sentimiento']:.2f})")
            elif resultados["sentimiento"] < -0.05:
                st.error(f"📉 Negativo ({resultados['sentimiento']:.2f})")
            else:
                st.info(f"📊 Neutral ({resultados['sentimiento']:.2f})")

            st.subheader("Subjetividad")
            st.progress(resultados["subjetividad"])
            if resultados["subjetividad"] > 0.5:
                st.warning(f"💭 Alta subjetividad ({resultados['subjetividad']:.2f})")
            else:
                st.info(f"📋 Baja subjetividad ({resultados['subjetividad']:.2f})")
    
    with col2:
        st.subheader("Palabras más frecuentes")
        if resultados["contador_palabras"]:
            df = pd.DataFrame(list(resultados["contador_palabras"].items())[:10], columns=["Palabra", "Frecuencia"])
            st.bar_chart(df.set_index("Palabra"), use_container_width=True)

    with st.container():
        st.subheader("Texto Traducido")
        with st.expander("Ver traducción completa"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Texto Original:**")
                st.text(resultados["texto_original"])
            with col2:
                st.markdown("**Texto Traducido:**")
                st.text(resultados["texto_traducido"])

    with st.container():
        st.subheader("Frases detectadas")
        for i, frase_dict in enumerate(resultados["frases"][:10], 1):
            frase_original = frase_dict["original"]
            frase_traducida = frase_dict["traducido"]
            blob_frase = TextBlob(frase_traducida)
            polaridad = blob_frase.sentiment.polarity
            emoji = "😊" if polaridad > 0.05 else "😟" if polaridad < -0.05 else "😐"
            st.markdown(f'<div class="recuadro">{i}. {emoji} <b>Original:</b> *"{frase_original}"*<br><b>Traducción:</b> *"{frase_traducida}"* (Sentimiento: {polaridad:.2f})</div>', unsafe_allow_html=True)


if modo == "Texto directo":
    st.subheader("Ingresa tu texto para analizar")
    texto = st.text_area("", height=200, placeholder="Escribe o pega aquí el texto que deseas analizar...")
    if st.button("Analizar texto"):
        if texto.strip():
            with st.spinner("Analizando texto..."):
                resultados = procesar_texto(texto)
                crear_visualizaciones(resultados)
        else:
            st.warning("Por favor, ingresa algún texto para analizar.")
elif modo == "Archivo de texto":
    st.subheader("Carga un archivo de texto")
    archivo = st.file_uploader("", type=["txt", "csv", "md"])
    if archivo is not None:
        try:
            contenido = archivo.getvalue().decode("utf-8")
            with st.expander("Ver contenido del archivo"):
                st.text(contenido[:1000] + ("..." if len(contenido) > 1000 else ""))
            if st.button("Analizar archivo"):
                with st.spinner("Analizando archivo..."):
                    resultados = procesar_texto(contenido)
                    crear_visualizaciones(resultados)
        except Exception as e:
            st.error(f"Error al procesar el archivo: {e}")

st.markdown("---")
st.markdown("Desarrollado con ❤️ usando Streamlit y TextBlob")
