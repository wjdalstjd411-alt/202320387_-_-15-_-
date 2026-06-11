import os
import pandas as pd

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)


def clear_graph(tx):
    tx.run("MATCH (n) DETACH DELETE n")


def create_company(tx, company_id, company_name, industry):
    tx.run(
        """
        MERGE (c:Company {id:$id})
        SET c.name=$name,
            c.industry=$industry
        """,
        id=company_id,
        name=company_name,
        industry=industry
    )


def create_person(tx, person_id, person_name):
    tx.run(
        """
        MERGE (p:Person {id:$id})
        SET p.name=$name
        """,
        id=person_id,
        name=person_name
    )


def create_university(tx, university_id, university_name):
    tx.run(
        """
        MERGE (u:University {id:$id})
        SET u.name=$name
        """,
        id=university_id,
        name=university_name
    )


with driver.session() as session:

    session.execute_write(clear_graph)

    companies = pd.read_csv("data/companies.csv")

    for _, row in companies.iterrows():
        session.execute_write(
            create_company,
            row["company_id"],
            row["company_name"],
            row["industry"]
        )

    people = pd.read_csv("data/people.csv")

    for _, row in people.iterrows():
        session.execute_write(
            create_person,
            row["person_id"],
            row["person_name"]
        )

    universities = pd.read_csv("data/universities.csv")

    for _, row in universities.iterrows():
        session.execute_write(
            create_university,
            row["university_id"],
            row["university_name"]
        )

    print("Graph Nodes Created!")

    relations = pd.read_csv("data/relations.csv")

    for _, row in relations.iterrows():

        source = row["source"]
        relation = row["relation"]
        target = row["target"]

        query = f"""
        MATCH (a {{name:$source}})
        MATCH (b {{name:$target}})
        MERGE (a)-[r:{relation}]->(b)
        """

        session.run(
            query,
            source=source,
            target=target
        )

    print("Relationships Created!")

driver.close()