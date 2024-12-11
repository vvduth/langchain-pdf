from threading import Thread
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.base import BaseCallbackHandler
from dotenv import load_dotenv
from queue import Queue


load_dotenv()

class StreamingHandler(BaseCallbackHandler):
    
    def __init__(self,queue):
        self.queue = queue
        
    def on_llm_new_token(self, token, **kwargs):
        self.queue.put(token)
    def on_llm_end(self, response, **kwargs):
        self.queue.put(None)
    def on_llm_error(self, error, *, run_id, parent_run_id = None, **kwargs):
        self.queue.put(None)
        
chat  = ChatOpenAI(streaming = True)

prompt = ChatPromptTemplate.from_messages([
    ("human", "{content}")
])

class StreamableChain:
    def stream(self, input, **kwargs):
        queue = Queue()
        handler = StreamingHandler(queue)
        
        def task():
            self(input, callbacks=[handler])
            
        Thread(target=task).start()
        
        while True:
            token = queue.get()
            if token is None:
                break
            yield(token)


class StreamingLLMChain(StreamableChain, LLMChain):
    pass

chain = StreamingLLMChain(llm=chat, prompt=prompt)

for output in chain.stream(input={"content": "name me a mix martail artist   in ufc and his record"}):
    print(output)