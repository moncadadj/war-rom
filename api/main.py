import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI()

# Root directory for absolute path resolution (fixes Vercel serverless paths)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configuration
def obtener_llave():
    api_key_env = os.environ.get("GEMINI_API_KEY")
    return api_key_env

api_key = obtener_llave()
if api_key:
    genai.configure(api_key=api_key)
else:
    print("Warning: No Gemini API Key found.")


CONTEXTO_LAB = """
Eres un Asesor Senior de RADLEADX.
Tu propósito es mejorar la CAPA DE INTELIGENCIA (RadLogic).
Analizamos cómo interpretar señales de intención humana en internet.
"""

class AgentRequest(BaseModel):
    role: str
    challenge: str

class DecreeRequest(BaseModel):
    nlu_response: str
    outreach_response: str
    business_response: str

@app.get("/", response_class=HTMLResponse)
async def read_root():
    template_path = os.path.join(BASE_DIR, "templates", "index.html")
    with open(template_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.post("/consult_agent")
async def consult_agent(req: AgentRequest):
    model = genai.GenerativeModel('gemini-1.5-flash')
    full_prompt = f"{CONTEXTO_LAB}\n\nActúa como {req.role}.\nDesafío: {req.challenge}"
    try:
        response = model.generate_content(full_prompt)
        return {"result": response.text}
    except Exception as e:
        return {"result": f"Error en el agente: {str(e)}"}

@app.post("/final_decree")
async def final_decree(req: DecreeRequest):
    juez = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"Sintetiza un plan de acción técnica para RadLeadX basado en:\nNLU: {req.nlu_response}\nOutreach: {req.outreach_response}\nBusiness: {req.business_response}"
    try:
        sintesis = juez.generate_content(prompt)
        return {"result": sintesis.text}
    except Exception as e:
        return {"result": f"Error en síntesis: {str(e)}"}
