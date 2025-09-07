from fastapi import FastAPI 
from langchain_deepseek import ChatDeepSeek 
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.output_parsers import StrOutputParser 
from langserve import add_routes 
from dotenv import load_dotenv 
import os 
from langchain_core.runnables import Runnable


load_dotenv() 
print("DeepSeek API Key:", os.getenv("DEEPSEEK_API_KEY")) 
# 1. Create prompt template 
system_template = "Translate the following into {language}:" 
prompt_template = ChatPromptTemplate.from_messages( [("system", system_template), ("user", "{text}")] )
# 2. Create model 
model = ChatDeepSeek(model="deepseek-chat") 
# 3. Create parser 
parser = StrOutputParser() 
# 4. Create chain 
chain = prompt_template | model | parser  
print("Input schema:", chain.input_schema.model_json_schema())
print("Output schema:", chain.output_schema.model_json_schema())
# 5. App definition 
app = FastAPI( title="LangChain Server", version="1.0", description="A simple API server using LangChain's Runnable interfaces", ) 
# 6. Adding chain route 
add_routes( app, chain, path="/chain", ) 
# 打印所有注册的路由
for route in app.routes:
    print(route.path, route.methods)
if __name__ == "__main__": 
    import uvicorn 
    uvicorn.run(app, host="0.0.0.0", port=8000)
    #print(chain.invoke({"language": "italian", "text": "hi"}))

