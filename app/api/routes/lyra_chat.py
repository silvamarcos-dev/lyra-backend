from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.routes.auth import get_current_user
from app.schemas.lyra_chat import (
    LyraChatRequest,
    LyraChatResponse,
    LyraChatHistoryResponse,
    LyraChatResetResponse,
)
from app.services.lyra_chat_service import chat_with_lyra
from app.data.repositories.chat_repository import (
    save_message,
    get_chat_history,
    clear_chat,
)

from app.services.calendar_intent_service import detect_calendar_intent
from app.services.calendar_query_intent_service import detect_calendar_query_intent
from app.integrations.calendar.google_calendar_service import (
    get_calendar_service,
    create_event_at_datetime,
    list_events_for_period,
)
from app.api.routes.calendar import google_token_store

router = APIRouter(prefix="/lyra", tags=["Lyra Chat"])


@router.post("/chat", response_model=LyraChatResponse)
def lyra_chat(
    request: LyraChatRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    save_message(db, user_id=current_user.id, role="user", content=request.message)

    calendar_query_intent = detect_calendar_query_intent(request.message)

    if calendar_query_intent:
        if not google_token_store:
            lyra_response = (
                "Sua Google Agenda ainda não está conectada. "
                "Vá em Google Agenda na Lyra e conecte sua conta primeiro."
            )

            save_message(
                db,
                user_id=current_user.id,
                role="assistant",
                content=lyra_response,
                mode="calendar_query"
            )

            return LyraChatResponse(
                user_message=request.message,
                lyra_response=lyra_response,
                mode_used="calendar_query"
            )

        service = get_calendar_service(google_token_store)
        events = list_events_for_period(
            service=service,
            period=calendar_query_intent["period"]
        )

        label = "hoje" if calendar_query_intent["period"] == "today" else "amanhã"

        if not events:
            lyra_response = f"Você não tem compromissos agendados para {label}."
        else:
            lines = []
            for event in events:
                start_info = event.get("start", {})
                start_value = start_info.get("dateTime") or start_info.get("date") or ""

                display_time = "Dia inteiro"
                if "T" in start_value:
                    try:
                        dt = datetime.fromisoformat(start_value.replace("Z", "+00:00"))
                        display_time = dt.astimezone().strftime("%H:%M")
                    except Exception:
                        display_time = start_value

                lines.append(f"• {display_time} - {event.get('summary', 'Evento sem título')}")

            lyra_response = (
                f"Você tem {len(events)} compromisso(s) para {label}:\n\n" +
                "\n".join(lines)
            )

        save_message(
            db,
            user_id=current_user.id,
            role="assistant",
            content=lyra_response,
            mode="calendar_query"
        )

        return LyraChatResponse(
            user_message=request.message,
            lyra_response=lyra_response,
            mode_used="calendar_query"
        )

    calendar_intent = detect_calendar_intent(request.message)

    if calendar_intent:
        if not google_token_store:
            lyra_response = (
                "Sua Google Agenda ainda não está conectada. "
                "Vá em Google Agenda na Lyra e conecte sua conta primeiro."
            )

            save_message(
                db,
                user_id=current_user.id,
                role="assistant",
                content=lyra_response,
                mode="calendar"
            )

            return LyraChatResponse(
                user_message=request.message,
                lyra_response=lyra_response,
                mode_used="calendar"
            )

        service = get_calendar_service(google_token_store)

        create_event_at_datetime(
            service=service,
            summary=calendar_intent["summary"],
            start_dt=calendar_intent["start_dt"],
            duration_minutes=calendar_intent["duration_minutes"],
        )

        lyra_response = (
            f"Perfeito. Adicionei na sua agenda para "
            f"{calendar_intent['start_dt'].strftime('%d/%m às %H:%M')}."
        )

        save_message(
            db,
            user_id=current_user.id,
            role="assistant",
            content=lyra_response,
            mode="calendar"
        )

        return LyraChatResponse(
            user_message=request.message,
            lyra_response=lyra_response,
            mode_used="calendar"
        )

    history = get_chat_history(db, current_user.id)

    formatted_history = [
        {"role": msg.role, "content": msg.content}
        for msg in history
    ]

    result = chat_with_lyra(
        message=request.message,
        conversation_history=formatted_history
    )

    save_message(
        db,
        user_id=current_user.id,
        role="assistant",
        content=result["lyra_response"],
        mode=result.get("mode_used")
    )

    return LyraChatResponse(
        user_message=result["user_message"],
        lyra_response=result["lyra_response"],
        mode_used=result["mode_used"]
    )


@router.get("/chat/history", response_model=LyraChatHistoryResponse)
def lyra_chat_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    history = get_chat_history(db, current_user.id)

    messages = [
        {
            "role": msg.role,
            "content": msg.content
        }
        for msg in history
    ]

    return LyraChatHistoryResponse(
        messages=messages,
        total=len(messages)
    )


@router.delete("/chat/history", response_model=LyraChatResetResponse)
def clear_lyra_chat_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    clear_chat(db, current_user.id)

    return LyraChatResetResponse(
        cleared=True,
        message="Histórico apagado com sucesso."
    )