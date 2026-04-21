from urllib.parse import urlencode

import requests
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse

from app.core.settings import (
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_REDIRECT_URI,
)
from app.integrations.calendar.google_calendar_service import (
    get_calendar_service,
    list_upcoming_events,
    create_event as create_google_event,
)

router = APIRouter(prefix="/calendar", tags=["Google Calendar"])

# MVP: token em memória
google_token_store: dict = {}


@router.get("/connect")
def connect_google():
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        raise HTTPException(status_code=500, detail="Google OAuth não configurado.")

    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "https://www.googleapis.com/auth/calendar",
        "access_type": "offline",
        "prompt": "consent",
    }

    auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urlencode(params)
    return RedirectResponse(auth_url)


@router.get("/callback")
def calendar_callback(code: str):
    token_url = "https://oauth2.googleapis.com/token"

    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    response = requests.post(token_url, data=data, timeout=30)
    token_data = response.json()

    if response.status_code >= 400:
        raise HTTPException(status_code=400, detail=token_data)

    google_token_store.clear()
    google_token_store.update(token_data)
    google_token_store["client_id"] = GOOGLE_CLIENT_ID
    google_token_store["client_secret"] = GOOGLE_CLIENT_SECRET

    return RedirectResponse("http://localhost:5173/calendar?connected=true")


@router.get("/events")
def get_events():
    if not google_token_store:
        raise HTTPException(status_code=401, detail="Google Agenda não conectada.")

    service = get_calendar_service(google_token_store)
    events = list_upcoming_events(service)

    return {
        "success": True,
        "total": len(events),
        "events": events,
    }


@router.post("/create")
def create_event(summary: str, minutes_from_now: int = 30, duration_minutes: int = 60):
    if not google_token_store:
        raise HTTPException(status_code=401, detail="Google Agenda não conectada.")

    service = get_calendar_service(google_token_store)
    event = create_google_event(
        service,
        summary=summary,
        minutes_from_now=minutes_from_now,
        duration_minutes=duration_minutes,
    )

    return {
        "success": True,
        "event": event,
    }