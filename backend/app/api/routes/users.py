from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
def me(user: User = Depends(get_current_user)) -> dict[str, object]:
    return {"id": user.id, "email": user.email, "is_active": user.is_active}
