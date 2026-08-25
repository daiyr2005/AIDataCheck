from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException, status
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama

from mysite.api.auth import get_current_user
from mysite.db.model import UserProfile, UserStatusChoice
from mysite.db.schema import ChatRequest, ChatResponse

agent_router = APIRouter(prefix="/ai_chat", tags=["Agent"])

model = ChatOllama(
    model="llama3.2",
    temperature=0,
)

FREE_REQUESTS_LIMIT = 1
_basic_usage: dict[int, int] = defaultdict(int)


@agent_router.post("/", response_model=ChatResponse)
async def chat_with_agent(
    payload: ChatRequest,
    current_user: UserProfile = Depends(get_current_user),
):
    if current_user.status == UserStatusChoice.basic.value:
        used = _basic_usage[current_user.id]

        if used >= FREE_REQUESTS_LIMIT:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "Бул функция pro тарифинде гана жеткиликтуу. "
                    "Сиздин акысыз суроо-талабыныздын лимити бутту."
                ),
            )

        _basic_usage[current_user.id] = used + 1


    messages = [
        SystemMessage(
            content=(
                "Ты очень опытный Python Senior разработчик с 10-летним опытом. "
                "Ты должен отвечать на вопросы кратко и с примерами."
                "Махсимум 3 пример"
            )
        ),
        HumanMessage(content=payload.message),
    ]

    result = model.invoke(messages)
    return ChatResponse(response=result.content)