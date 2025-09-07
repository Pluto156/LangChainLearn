from fastapi import FastAPI 
from langchain_deepseek import ChatDeepSeek 
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.output_parsers import StrOutputParser 
from langserve import add_routes 
from dotenv import load_dotenv 
import os 
from langchain_core.runnables import Runnable
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, trim_messages
from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.runnables import RunnablePassthrough
from operator import itemgetter
load_dotenv() 
print("DeepSeek API Key:", os.getenv("DEEPSEEK_API_KEY")) 

model = ChatDeepSeek(model="deepseek-chat") 

store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

trimmer = trim_messages(
    max_tokens=65,
    strategy="last",
    token_counter=model,
    include_system=True,
    allow_partial=False,
    start_on="human",
)
config = {"configurable": {"session_id": "abc2"}}

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Answer all questions to the best of your ability in {language}.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# chain = (
#     RunnablePassthrough.assign(messages=itemgetter("messages") | trimmer)
#     | prompt
#     | model
# )
chain = (
    prompt
    | model
)
with_message_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="messages",
)
# response = with_message_history.invoke(
#     {"messages": [HumanMessage(content="hi! I'm todd")], "language": "Japanese"},
#     config=config,
# )
# print(response.content)

for r in with_message_history.stream(
    {
        "messages": [HumanMessage(content="hi! I'm todd. tell me a joke")],
        "language": "English",
    },
    config=config,
):
    print(r.content, end="|")