from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai.registry import get_provider
from app.api.deps import get_db
from app.core.dependencies import get_current_user
from app.models.conversation import Conversation, Message
from app.models.user import User

router = APIRouter(prefix="/conversations", tags=["conversations"])


class CreateConversationRequest(BaseModel):
    title: str = Field(default="New conversation", min_length=1, max_length=200)


class MessageRequest(BaseModel):
    content: str = Field(min_length=1, max_length=20000)
    provider: str = "mock"
    model: str | None = None


@router.get("")
def list_conversations(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.scalars(select(Conversation).where(Conversation.user_id == user.id).order_by(Conversation.updated_at.desc())).all()


@router.post("")
def create_conversation(payload: CreateConversationRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    conversation = Conversation(user_id=user.id, title=payload.title)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation


@router.get("/{conversation_id}/messages")
def list_messages(conversation_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    conversation = db.scalar(select(Conversation).where(Conversation.id == conversation_id, Conversation.user_id == user.id))
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return db.scalars(select(Message).where(Message.conversation_id == conversation.id).order_by(Message.created_at)).all()


@router.post("/{conversation_id}/messages")
async def send_message(conversation_id: int, payload: MessageRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    conversation = db.scalar(select(Conversation).where(Conversation.id == conversation_id, Conversation.user_id == user.id))
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    user_message = Message(conversation_id=conversation.id, role="user", content=payload.content)
    db.add(user_message)
    provider = get_provider(payload.provider)
    result = await provider.generate(payload.content, payload.model)
    assistant_message = Message(conversation_id=conversation.id, role="assistant", content=result.content, provider=result.provider, model=result.model)
    db.add(assistant_message)
    db.commit()
    db.refresh(assistant_message)
    return assistant_message
