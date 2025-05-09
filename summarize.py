from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.documents import Document
from langchain_ollama import OllamaLLM
from typing import Dict, List, Any


def extract_pros_and_cons(reviews: List[str], models: Dict[str, Any] = {}) -> Dict[str, str]:
    """Extract pros and cons from restaurant reviews using Ollama LLM."""
    # Use a lightweight model that requires minimal memory
    llm = OllamaLLM(
        model="llama3.2",
        temperature=0.5
    )

    # Convert reviews to Document objects for LangChain
    documents = [Document(page_content=review) for review in reviews]

    # Create prompt templates for pros and cons
    pros_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a sentiment analyst. Based only on the following reviews, identify genuine **positive aspects** of the restaurant.

    Write 3 to 5 clear bullet points only. Do not include anything negative. Avoid repetition.

    Reviews:
    {context}""")
    ])
    cons_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a sentiment analyst. Based only on the following reviews, identify genuine **negative aspects** of the restaurant.

    Write 3 to 5 clear bullet points only. Do not include anything positive. Avoid repetition.

    Reviews:
    {context}""")
    ])

    # Create chains for pros and cons
    pros_chain = create_stuff_documents_chain(llm, pros_prompt)
    cons_chain = create_stuff_documents_chain(llm, cons_prompt)

    # Execute chains
    pros_result = pros_chain.invoke({"context": documents})
    cons_result = cons_chain.invoke({"context": documents})

    return {
        "pros": pros_result,
        "cons": cons_result
    }