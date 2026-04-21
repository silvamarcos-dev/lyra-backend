# 🚀 Lyra Core

Núcleo central de uma inteligência artificial multiagente, modular e evolutiva.

## 🧠 Visão Geral

Lyra é uma arquitetura de IA capaz de:

- Criar agentes especializados
- Gerenciar memória inteligente
- Orquestrar múltiplos agentes
- Evoluir com base em interações
- Servir como base para sistemas de IA personalizados

## ⚙️ Stack

- Python (FastAPI)
- Pydantic
- Uvicorn
- React + Vite
- TailwindCSS

## 🔥 Funcionalidades

- Criação de agentes inteligentes
- Memória persistente por agente
- Extração de tags e objetivos
- Orquestração multiagente
- Interface operacional (dashboard)

## 📦 Estrutura

app/
    core/
    routes/
    services/
    data/
    schemas/

## 🚀 Como rodar

### Backend

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn main:app --reload

### Frontend
    npm install 
    npm run dev

### Instalações futuras

- Integração com as seguintes APIs
. CLAUDE - para a geração de códigos
. GEMINI - para geração de imagens 
. OPENAI - chat e geração de textos, pesquisas etc
