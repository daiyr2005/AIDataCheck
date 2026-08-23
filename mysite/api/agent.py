from fastapi import APIRouter
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from mysite.db.schema import ChatRequest, ChatResponse

agent_router = APIRouter(prefix="/ai_chat", tags=["Agent"])

model = ChatOllama(
    model="llama3.2",
    temperature=0
)


@agent_router.post("/", response_model=ChatResponse)
async def chat_with_agent(payload: ChatRequest):
    messages = [
        SystemMessage(
            content="Ты очень опытный Python Senior разработчик с 10-летним опытом. Ты должен отвечать на вопросы кратко и с примерами."
        ),
        HumanMessage(content=payload.message)
    ]

    result = model.invoke(messages)
    return ChatResponse(response=result.content)