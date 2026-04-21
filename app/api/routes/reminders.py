from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.routes.auth import get_current_user
from app.schemas.reminder import (
    ReminderCreateRequest,
    ReminderResponse,
    ReminderListResponse,
)
from app.data.repositories.reminder_repository import (
    create_reminder,
    list_user_reminders,
)

router = APIRouter(prefix="/reminders", tags=["Reminders"])


@router.post("/", response_model=ReminderResponse)
def create_user_reminder(
    request: ReminderCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    reminder = create_reminder(
        db=db,
        user_id=current_user.id,
        title=request.title,
        description=request.description,
        remind_at=request.remind_at,
        channel=request.channel,
    )

    return ReminderResponse(
        id=reminder.id,
        title=reminder.title,
        description=reminder.description,
        remind_at=reminder.remind_at,
        channel=reminder.channel,
        status=reminder.status,
        sent=reminder.sent,
    )


@router.get("/", response_model=ReminderListResponse)
def get_user_reminders(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    reminders = list_user_reminders(db, current_user.id)

    return ReminderListResponse(
        reminders=[
            ReminderResponse(
                id=item.id,
                title=item.title,
                description=item.description,
                remind_at=item.remind_at,
                channel=item.channel,
                status=item.status,
                sent=item.sent,
            )
            for item in reminders
        ],
        total=len(reminders),
    )