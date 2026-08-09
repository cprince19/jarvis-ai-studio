from pydantic import BaseModel, Field


class WorkflowCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=5000)


class WorkflowResponse(BaseModel):
    id: int
    name: str
    description: str | None
    status: str

    model_config = {"from_attributes": True}
