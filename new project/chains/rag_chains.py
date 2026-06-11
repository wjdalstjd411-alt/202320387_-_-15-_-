from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)

def ask_rag(question, retriever):

    docs = retriever.invoke(question)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
Answer only using the provided context.

Context:
{context}

Question:
{question}
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "contexts": [doc.page_content for doc in docs]
    }