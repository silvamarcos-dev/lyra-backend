from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.auth import router as auth_router
from app.api.routes.agents import router as agents_router
from app.api.routes.lyra_chat import router as lyra_chat_router
from app.api.routes.legal import router as legal_router
from app.api.routes.reminders import router as reminders_router
from app.api.routes.reminder_dispatch import router as reminder_dispatch_router
from app.api.routes.whatsapp_webhook import router as whatsapp_webhook_router
from app.api.routes.calendar import router as calendar_router

app = FastAPI(title="Lyra Core API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://blond-ryan-vehicles-loud.trycloudflare.com",
        "https://lyra-aurion-system.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(agents_router)
app.include_router(lyra_chat_router)
app.include_router(legal_router)
app.include_router(reminders_router)
app.include_router(reminder_dispatch_router)
app.include_router(whatsapp_webhook_router)
app.include_router(calendar_router)


@app.get("/")
def root():
    return {
        "name": "Lyra Core API",
        "version": "0.1 Pré-Release",
        "status": "online"
    }