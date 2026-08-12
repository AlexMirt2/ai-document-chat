from pydantic import BaseModel, Field


class HistoryMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    document_id: int
    history: list[HistoryMessage] = Field(default_factory=list)


class Source(BaseModel):
    page: int
    document_id: int


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]