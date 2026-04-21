from datetime import datetime, timedelta, timezone

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_calendar_service(token_data: dict):
    creds = Credentials(
        token=token_data["access_token"],
        refresh_token=token_data.get("refresh_token"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=token_data["client_id"],
        client_secret=token_data["client_secret"],
        scopes=SCOPES,
    )
    return build("calendar", "v3", credentials=creds)


def list_upcoming_events(service, max_results: int = 10):
    now = datetime.now(timezone.utc).isoformat()

    events_result = service.events().list(
        calendarId="primary",
        timeMin=now,
        maxResults=max_results,
        singleEvents=True,
        orderBy="startTime",
    ).execute()

    return events_result.get("items", [])


def list_events_for_period(service, period: str = "today", max_results: int = 20):
    now = datetime.now().astimezone()

    if period == "today":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)
    elif period == "tomorrow":
        start = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)
    else:
        start = now
        end = now + timedelta(days=1)

    events_result = service.events().list(
        calendarId="primary",
        timeMin=start.astimezone(timezone.utc).isoformat(),
        timeMax=end.astimezone(timezone.utc).isoformat(),
        maxResults=max_results,
        singleEvents=True,
        orderBy="startTime",
    ).execute()

    return events_result.get("items", [])


def create_event(service, summary: str, minutes_from_now: int = 30, duration_minutes: int = 60):
    start = datetime.now(timezone.utc) + timedelta(minutes=minutes_from_now)
    end = start + timedelta(minutes=duration_minutes)

    event_body = {
        "summary": summary,
        "start": {
            "dateTime": start.isoformat(),
            "timeZone": "UTC",
        },
        "end": {
            "dateTime": end.isoformat(),
            "timeZone": "UTC",
        },
    }

    created_event = service.events().insert(
        calendarId="primary",
        body=event_body,
    ).execute()

    return created_event


def create_event_at_datetime(service, summary: str, start_dt: datetime, duration_minutes: int = 60):
    end_dt = start_dt + timedelta(minutes=duration_minutes)

    event_body = {
        "summary": summary,
        "start": {
            "dateTime": start_dt.isoformat(),
            "timeZone": "America/Sao_Paulo",
        },
        "end": {
            "dateTime": end_dt.isoformat(),
            "timeZone": "America/Sao_Paulo",
        },
    }

    created_event = service.events().insert(
        calendarId="primary",
        body=event_body,
    ).execute()

    return created_event