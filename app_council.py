import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime

# --- 1. CONFIGURACIÓN DE INTERFAZ (DISEÑO STITCH) ---
st.set_page_config(page_title="RADLEADX | AI Strategy Lab", layout="wide", page_icon="🧠")

# Inyección de CSS para emular el prototipo de Stitch
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700&display=swap');
    
    /* Estética Dark Mode de alta fidelidad - War Room */
    .stApp { background-color: #080808; color: #e5e2e1; font-family: 'Inter', sans-serif; }
    
    /* Contenedores de Agentes (Las Oficinas) */
    .agent-card {
        border-radius: 24px; /* rounded-xl */
        padding: 24px;
        background-color: #161616;
        border: 1px solid #2C2C2E;
        min-height: 450px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }
    
    /* Colores de acento por oficina */
    .nlu-office { border-top: 4px solid #007AFF; }
    .outreach-office { border-top: 4px solid #34C759; }
    .scaling-office { border-top: 4px solid #AF52DE; }
    
    /* Títulos y fuentes */
    .agent-header {
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        font-size: 12px; /* label-caps */
        margin-bottom: 15px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    p, div, span {
        font-family: 'Inter', sans-serif;
    }
    
    /* Logs text inside agents */
    .agent-card p:not(.agent-header) {
        font-family: 'JetBrains Mono', monospace;
        font-size: 14px;
        color: #c1c6d7;
    }
    
    /* Título principal */
    h1 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
    }
    
    /* Dictamen Final */
    .final-decree {
        background-color: #161616;
        border: 1px solid #2C2C2E;
        border-left: 4px solid #adc6ff;
        padding: 30px;
        border-radius: 16px; /* rounded-lg */
        font-family: 'Inter', sans-serif;
        line-height: 1.6;
        color: #e5e2e1;
    }
    
    /* Ajustes botones y entradas */
    .stButton>button {
        border-radius: 16px;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        background-color: #4b8eff;
        color: #00285c;
        border: none;
    }
    .stButton>button:hover {
        background-color: #adc6ff;
        color: #002e69;
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #1c1b1b;
        border: 1px solid #414755;
        color: #e5e2e1;
        border-radius: 16px;
        font-family: 'Inter', sans-serif;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #4b8eff;
        box-shadow: none;
    }
    
    hr {
        border-top: 1px solid #2C2C2E;
    }
    </style>
    """, unsafe_allow_html=True)


# --- 2. GESTIÓN DE CREDENCIALES (API KEY SEGURA) ---
def obtener_llave():
    # Intenta leer de st.secrets (Streamlit Cloud)
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
        
    # Intenta leer de variables de entorno (Vercel, local env)
    api_key_env = os.environ.get("GEMINI_API_KEY")
    if api_key_env:
        return api_key_env
        
    # Intenta leer el archivo api_key.txt como fallback final local
    if os.path.exists("api_key.txt"):
        with open("api_key.txt", "r") as f:
            return f.read().strip()
            
    return None

api_key = obtener_llave()
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("No se encontró la API Key de Gemini. Por favor configúrala en st.secrets, en las variables de entorno como GEMINI_API_KEY, o en el archivo api_key.txt")
    st.stop()

if not os.path.exists("historial"):
    os.makedirs("historial")

# --- 3. CORE DE ASESORÍA ESTRATÉGICA ---
CONTEXTO_LAB = """
Eres un Asesor Senior de RADLEADX. 
Tu propósito es mejorar la CAPA DE INTELIGENCIA (RadLogic).
Analizamos cómo interpretar señales de intención humana en internet.
"""

def consultar_consejo(rol, desafio):
    model = genai.GenerativeModel('models/gemini-1.5-flash')
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
            res_nlu = consultar_consejo('Especialista en NLU y Semántica de Intención', desafio_estudio)
            st.markdown(f'<div class=\"agent-card nlu-office\"><p class=\"agent-header\" style=\"color:#007AFF;\">🔍 RadLogic Optimizator</p><p>{res_nlu}</p></div>', unsafe_allow_html=True)
        
        # OFICINA 2: OUTREACH
        with col2:
            res_out = consultar_consejo('Estratega de Conversión Contextual', desafio_estudio)
            st.markdown(f'<div class=\"agent-card outreach-office\"><p class=\"agent-header\" style=\"color:#34C759;\">📧 Outreach Architect</p><p>{res_out}</p></div>', unsafe_allow_html=True)
            
        # OFICINA 3: SCALING
        with col3:
            res_biz = consultar_consejo('Arquitecto de Monetización B2B', desafio_estudio)
            st.markdown(f'<div class=\"agent-card scaling-office\"><p class=\"agent-header\" style=\"color:#AF52DE;\">🚀 Scaling Strategist</p><p>{res_biz}</p></div>', unsafe_allow_html=True)

    # FASE: DICTAMEN FINAL (NOTEBOOKLM)
    st.divider()
    st.subheader("⚖️ Dictamen Final del Presidente del Consejo")
    
    juez = genai.GenerativeModel('models/gemini-1.5-flash')
    sintesis = juez.generate_content(f"Sintetiza un plan de acción técnica para RadLeadX basado en: {res_nlu} {res_out} {res_biz}").text
    
    st.markdown(f'<div class="final-decree">{sintesis}</div>', unsafe_allow_html=True)
    
    # Auto-guardado
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    with open(f"historial/Estudio_{ts}.md", "w", encoding="utf-8") as f:
        f.write(f"# DESAFÍO: {desafio_estudio}\n\n{sintesis}") 
    st.markdown(f'<div class="final-decree">{sintesis}</div>', unsafe_allow_html=True)
    
    # Auto-guardado
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    with open(f"historial/Estudio_{ts}.md", "w", encoding="utf-8") as f:
        f.write(f"# DESAFÍO: {desafio_estudio}\n\n{sintesis}")
