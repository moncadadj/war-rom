import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI()

# Configuration
def obtener_llave():
    api_key_env = os.environ.get("GEMINI_API_KEY")
    if api_key_env:
        return api_key_env
    if os.path.exists("api_key.txt"):
        with open("api_key.txt", "r") as f:
            return f.read().strip()
    return None

api_key = obtener_llave()
if api_key:
    genai.configure(api_key=api_key)
else:
    print("Warning: No Gemini API Key found.")

templates = Jinja2Templates(directory="templates")

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
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/api/consult_agent")
async def consult_agent(req: AgentRequest):
    model = genai.GenerativeModel('gemini-1.5-flash')
    full_prompt = f"{CONTEXTO_LAB}\n\nActúa como {req.role}.\nDesafío: {req.challenge}"
    try:
        response = model.generate_content(full_prompt)
        return {"result": response.text}
    except Exception as e:
        return {"result": f"Error en el agente: {str(e)}"}

@app.post("/api/final_decree")
async def final_decree(req: DecreeRequest):
    juez = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"Sintetiza un plan de acción técnica para RadLeadX basado en:\nNLU: {req.nlu_response}\nOutreach: {req.outreach_response}\nBusiness: {req.business_response}"
    try:
        sintesis = juez.generate_content(prompt)
        return {"result": sintesis.text}
    except Exception as e:
        return {"result": f"Error en síntesis: {str(e)}"}
