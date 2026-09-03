from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage
from langchain_ollama import ChatOllama

# Инициализируем модель (убедитесь, что выполнили: ollama run llama3.2)
model = ChatOllama(
    model='llama3.2',
    temperature=0
)

messages = [
    SystemMessage(
        content=(
            'Ты очень опытный python senior разработчик с 10 летним опытом. '
            'Ты должен отвечать на вопросы кратко и с примерами'
            'количество предложения максимум 3'
        )
    ),
    HumanMessage(
        content='что такое langchain?'
    )
]

response = model.invoke(messages)

#print(type(response))
print(response.content)