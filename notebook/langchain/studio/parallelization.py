from operator import add
from typing import Annotated
from typing_extensions import TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.document_loaders import WikipediaLoader
from langchain_community.tools import TavilySearchResults
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

llm = ChatOpenAI(model="gpt-4o-mini")

class State(TypedDict):
    question: str
    answer: str
    context: Annotated[list[str], add]
    
def search_tavily(state: State):
    tavily_search = TavilySearchResults(max_results=2)
    search_docs = tavily_search.invoke(state["question"])
    
    formatted_content = "\n---\n".join([
        f"Title: {doc['title']} \n Content: {doc['content']}"
        for doc in search_docs
    ])
    
    return {"context": [formatted_content]}
    

def search_web(state: State):
    search_docs = WikipediaLoader(query=state["question"], load_max_docs=2).load()
    
    formatted_content = "\n---\n".join([
        f"Title: {doc.metadata['title']} \n Content: {doc.page_content}"
        for doc in search_docs
    ])
    
    return {"context": [formatted_content]}

def generate_answer(state: State):
    
    question = state["question"]
    context = state["context"]
    
    prompt = f"Answer the question: {question} based on the context: {context}"
    answer = llm.invoke([SystemMessage(content=prompt)] + [HumanMessage(content=question)])
    
    return {"answer": answer}


# Add nodes
builder = StateGraph(State)

builder.add_node("search_tavily",search_tavily)
builder.add_node("search_web", search_web)
builder.add_node("generate_answer", generate_answer)

builder.add_edge(START, "search_web")
builder.add_edge(START, "search_tavily")
builder.add_edge("search_web", "generate_answer")
builder.add_edge("search_tavily", "generate_answer")
builder.add_edge("generate_answer", END)
graph = builder.compile()

