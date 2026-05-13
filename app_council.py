import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime

# --- 1. CONFIGURACIÓN DE INTERFAZ (DISEÑO STITCH) ---
st.set_page_config(page_title="RADLEADX | AI Strategy Lab", layout="wide", page_icon="🧠")

# Inyección de CSS para emular el prototipo de Stitch
st.markdown("""
    <style>
    /* Estética Dark Mode de alta fidelidad */
    .stApp { background-color: #0b0e14; color: #e6edf3; }
    
    /* Contenedores de Agentes (Las Oficinas) */
    .agent-card {
        border-radius: 12px;
        padding: 24px;
        background-color: #161b22;
        border: 1px solid #30363d;
        min-height: 450px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    
    /* Colores de acento por oficina */
    .nlu-office { border-top: 5px solid #58a6ff; }
    .outreach-office { border-top: 5px solid #3fb950; }
    .scaling-office { border-top: 5px solid #bc8cff; }
    
    /* Títulos y fuentes */
    .agent-header {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 15px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Dictamen Final (Estilo NotebookLM) */
    .final-decree {
        background-color: #0d1117;
        border: 1px solid #ff4b4b;
        padding: 30px;
        border-radius: 10px;
        font-family: 'Georgia', serif;
        line-height: 1.6;
        color: #c9d1d9;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. GESTIÓN DE CREDENCIALES (API KEY FIJA) ---
def obtener_llave():
    # Intenta leer el archivo api_key.txt primero
    if os.path.exists("api_key.txt"):
        with open("api_key.txt", "r") as f:
            return f.read().strip()
    # Si no, usa la clave que me pasaste (ajustada para ser reconocida)
    return "AIzaSyCx1mFz_ePuQrLm5y_yz0eNd-l2_jNOnNI"

api_key = obtener_llave()
if api_key:
    genai.configure(api_key=api_key)

if not os.path.exists("historial"):
    os.makedirs("historial")

# --- 3. CORE DE ASESORÍA ESTRATÉGICA ---
CONTEXTO_LAB = """
Eres un Asesor Senior de RADLEADX. 
Tu propósito es mejorar la CAPA DE INTELIGENCIA (RadLogic).
Analizamos cómo interpretar señales de intención humana en internet.
"""

def consultar_consejo(rol, desafio):
    model = genai.GenerativeModel('models/gemini-3.1-flash-lite')
    full_prompt = f"{CONTEXTO_LAB}\n\nActúa como {rol}.\nDesafío: {desafio}"
    try:
        return model.generate_content(full_prompt).text
    except Exception as e:
        return f"Error en el agente: {str(e)}"

# --- 4. ESTRUCTURA VISUAL DEL WAR ROOM ---

# Sidebar: Historial persistente
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Angular_full_color_logo.svg/2048px-Angular_full_color_logo.svg.png", width=50) # Placeholder logo
    st.title("Logs de Sesión")
    st.markdown("---")
    logs = sorted(os.listdir("historial"), reverse=True)
    for log in logs[:8]:
        if st.button(f"📄 {log}", key=log, use_container_width=True):
            with open(f"historial/{log}", "r", encoding="utf-8") as f:
                st.info(f.read())

# Título Principal
st.markdown('<h1 style="color:#f0f6fc;">🏛️ RADLEADX <span style="color:#ff4b4b;">Strategy Lab</span></h1>', unsafe_allow_html=True)
st.caption("Entorno Privado de I+D para la Optimización de RadLogic")

# Módulo de Entrada (Stitch Style)
desafio_estudio = st.text_area("Describa el concepto o falla estratégica a analizar por el consejo:", 
                               placeholder="Ej: Análisis de señales de intención en foros de tecnología...")

if st.button("🧪 INICIAR DELIBERACIÓN", use_container_width=True):
    # FASE: OFICINAS DE AGENTES
    col1, col2, col3 = st.columns(3)
    
    with st.spinner("Los agentes están procesando la consulta..."):
        # OFICINA 1: NLU
        with col1:
            st.markdown('<div class="agent-card nlu-office">', unsafe_allow_html=True)
            st.markdown('<p class="agent-header" style="color:#58a6ff;">🔍 RadLogic Optimizator</p>', unsafe_allow_html=True)
            res_nlu = consultar_consejo("Especialista en NLU y Semántica de Intención", desafio_estudio)
            st.write(res_nlu)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # OFICINA 2: OUTREACH
        with col2:
            st.markdown('<div class="agent-card outreach-office">', unsafe_allow_html=True)
            st.markdown('<p class="agent-header" style="color:#3fb950;">📧 Outreach Architect</p>', unsafe_allow_html=True)
            res_out = consultar_consejo("Estratega de Conversión Contextual", desafio_estudio)
            st.write(res_out)
            st.markdown('</div>', unsafe_allow_html=True)
            
        # OFICINA 3: SCALING
        with col3:
            st.markdown('<div class="agent-card scaling-office">', unsafe_allow_html=True)
            st.markdown('<p class="agent-header" style="color:#bc8cff;">🚀 Scaling Strategist</p>', unsafe_allow_html=True)
            res_biz = consultar_consejo("Arquitecto de Monetización B2B", desafio_estudio)
            st.write(res_biz)
            st.markdown('</div>', unsafe_allow_html=True)

    # FASE: DICTAMEN FINAL (NOTEBOOKLM)
    st.divider()
    st.subheader("⚖️ Dictamen Final del Presidente del Consejo")
    
    juez = genai.GenerativeModel('models/gemini-3.1-flash-lite')
    sintesis = juez.generate_content(f"Sintetiza un plan de acción técnica para RadLeadX basado en: {res_nlu} {res_out} {res_biz}").text
    
    st.markdown(f'<div class="final-decree">{sintesis}</div>', unsafe_allow_html=True)
    
    # Auto-guardado
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    with open(f"historial/Estudio_{ts}.md", "w", encoding="utf-8") as f:
        f.write(f"# DESAFÍO: {desafio_estudio}\n\n{sintesis}")