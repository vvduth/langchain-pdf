from functools import partial
from .pinecone import build_retriever

retriever_map = {
    "pinecode_2": partial(build_retriever, k=2),
    "pinecode_1": partial(build_retriever, k=1),
    "pinecode_3": partial(build_retriever, k=3),
}