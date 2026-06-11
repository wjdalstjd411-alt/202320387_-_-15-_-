import os

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_neo4j import Neo4jGraph
from langchain_neo4j.chains.graph_qa.cypher import GraphCypherQAChain

load_dotenv()

graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
    database="5a8433a3"
)

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0
)

chain = GraphCypherQAChain.from_llm(
    llm=llm,
    graph=graph,
    verbose=True,
    allow_dangerous_requests=True
)

while True:

    question = input("\n질문 입력(q 종료): ")


    if question.lower() == "q":
        break

    result = chain.invoke(
        {"query": question}
    )

    print("\n답변:")
    print(result["result"])