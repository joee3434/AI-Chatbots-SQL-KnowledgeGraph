from neo4j import GraphDatabase

class Neo4jClient:
    def __init__(self, uri: str, user: str, password: str):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def run(self, cypher: str, params: dict | None = None):
        with self._driver.session() as session:
            result = session.run(cypher, params or {})
            return [record.data() for record in result]
