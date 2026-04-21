from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.routes.auth import get_current_user
from app.services.reminder_dispatch_service import dispatch_due_reminders

router = APIRouter(prefix="/reminders", tags=["Reminder Dispatch"])


@router.post("/dispatch")
def dispatch_reminders(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = dispatch_due_reminders(db)

    return {
        "success": True,
        "message": "Dispatcher executado com sucesso.",
        **result,
    }