from langchain.chains import ConversationalRetrievalChain   
from app.chat.chains.streamable import StreamableChain
from app.chat.chains.tracable import TraceablChain

class StreamingConversationalRetrievalChain(
   TraceablChain, StreamableChain,ConversationalRetrievalChain
):
    pass