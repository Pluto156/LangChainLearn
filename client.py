import httpx

url = "http://127.0.0.1:8000/chain/invoke"

from langserve import RemoteRunnable

remote_chain = RemoteRunnable("http://127.0.0.1:8000/chain")
result = remote_chain.invoke({"language": "italian", "text": "hi"})
print(result)