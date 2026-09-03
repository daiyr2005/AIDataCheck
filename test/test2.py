from langchain.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from time import perf_counter
from langchain_core.prompts import ChatPromptTemplate



prompt = ChatPromptTemplate.from_messages(
    [
        (
            'system',
            'Ты преподаватель {language}.'
            'Объяснай материал для уровня {level}.'
            'Всегда приводи пример кода',
        ),
        (
            'human',
            'Объясни тему: {topic}'
        )
    ]
)

model = ChatOllama(
    model='llama3.2:latest',
    temperature=0
)

chain = prompt | model

response = {
        "language": "Python",
        "level": "средний",
        "topic": 'Функция'
    }

for i in chain.stream(response):
    print(i.text, end='')





#
# start_time = perf_counter()
# first_chunk: float | None = None
# full_response = None
#
# model = ChatOllama(
#     model='llama3.2:latest',
#     temperature=0
# )
#
# message = [
#     SystemMessage(
#         content='Более подробно'
#     ),
#     HumanMessage(
#         content='Python это ...'
#     )
# ]
#
# for i in model.stream(message):
#
#     if i.text and first_chunk is None:
#         first_chunk = perf_counter()
#
#     print(i.text, end='', flush=True)
#
#     full_response = i if full_response is None else full_response + i
#
# finish_time = perf_counter()
#
# if full_response is not None:
#     ttft = first_chunk - start_time
#     print(f'TTFT: {round(ttft, 2)} sec')
#
#     total_time = finish_time - start_time
#     print(f'Total Time: {total_time:.2f} sec')