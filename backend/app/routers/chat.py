from fastapi import APIRouter

from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
)

from app.services.chat_service import ChatService


router = APIRouter(
    prefix="/api/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
):

    result = ChatService.ask(
        message=request.message,
        document_id=request.document_id,
        history=[
            {
                "role": message.role,
                "content": message.content,
            }
            for message in request.history
        ],
    )

    return ChatResponse(
        answer=result["answer"],
        sources=result["sources"],
    )