import os
from dotenv import load_dotenv

load_dotenv()

from neo4j import GraphDatabase

uri = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

print("PASSWORD:", repr(password))
print("PASSWORD:", password)
print("URI:", uri)
print("USERNAME:", username)

driver = GraphDatabase.driver(
    uri,
    auth=(username, password)
)

with driver.session() as session:
    result = session.run("RETURN 1 AS ok")
    print(result.single()["ok"])

driver.close()