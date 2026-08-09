from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.workflow import Workflow
from app.schemas.workflow import WorkflowCreate, WorkflowResponse

router = APIRouter(prefix="/workflows", tags=["workflows"])


@router.get("", response_model=list[WorkflowResponse])
def list_workflows(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return list(db.scalars(select(Workflow).where(Workflow.owner_id == user.id).order_by(Workflow.id.desc())))


@router.post("", response_model=WorkflowResponse, status_code=status.HTTP_201_CREATED)
def create_workflow(payload: WorkflowCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    workflow = Workflow(owner_id=user.id, name=payload.name, description=payload.description)
    db.add(workflow)
    db.commit()
    db.refresh(workflow)
    return workflow
