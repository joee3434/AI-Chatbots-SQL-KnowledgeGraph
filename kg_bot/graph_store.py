from neo4j_client import Neo4jClient

class GraphStore:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="password123"):
        self.db = Neo4jClient(uri, user, password)

    def close(self):
        self.db.close()

    @staticmethod
    def _value_key(entity: str, relation: str) -> str:
        return f"{entity.strip().lower()}::{relation.strip().lower()}"

    def add_fact(self, entity: str, relation: str, value: str) -> str:
        key = self._value_key(entity, relation)
        cypher = """
        MERGE (e:Entity {name: $entity})
        MERGE (v:Value {key: $key})
        SET v.value = $value
        MERGE (e)-[r:HAS {relation: $relation}]->(v)
        RETURN e.name AS entity, r.relation AS relation, v.value AS value
        """
        res = self.db.run(cypher, {"entity": entity, "relation": relation, "value": value, "key": key})
        if not res:
            return "No changes were made."
        row = res[0]
        return f"Stored fact: {row['entity']} {row['relation']} {row['value']}."

    def inquire(self, entity: str | None = None, relation: str | None = None) -> str:
        if entity and relation:
            cypher = """
            MATCH (e:Entity {name: $entity})-[r:HAS {relation: $relation}]->(v:Value)
            RETURN e.name AS entity, r.relation AS relation, v.value AS value
            """
            params = {"entity": entity, "relation": relation}
        elif entity:
            cypher = """
            MATCH (e:Entity {name: $entity})-[r:HAS]->(v:Value)
            RETURN e.name AS entity, r.relation AS relation, v.value AS value
            ORDER BY r.relation
            """
            params = {"entity": entity}
        else:
            cypher = """
            MATCH (e:Entity)-[r:HAS]->(v:Value)
            RETURN e.name AS entity, r.relation AS relation, v.value AS value
            ORDER BY e.name, r.relation
            """
            params = {}

        res = self.db.run(cypher, params)
        if not res:
            return "No facts found."

        lines = []
        for row in res:
            lines.append(f"{row['entity']} {row['relation']} {row['value']}")
        return "\n".join(lines)

    def update_fact(self, entity: str, relation: str, new_value: str) -> str:
        key = self._value_key(entity, relation)
        cypher = """
        MATCH (e:Entity {name: $entity})-[r:HAS {relation: $relation}]->(v:Value {key: $key})
        SET v.value = $new_value
        RETURN e.name AS entity, r.relation AS relation, v.value AS value
        """
        res = self.db.run(cypher, {"entity": entity, "relation": relation, "new_value": new_value, "key": key})
        if not res:
            return "Nothing to update (fact not found)."
        row = res[0]
        return f"Updated fact: {row['entity']} {row['relation']} {row['value']}."

    def delete_fact(self, entity: str, relation: str) -> str:
        key = self._value_key(entity, relation)
        cypher = """
        MATCH (e:Entity {name: $entity})-[r:HAS {relation: $relation}]->(v:Value {key: $key})
        DELETE r
        WITH v
        OPTIONAL MATCH (v)<-[r2:HAS]-()
        WITH v, count(r2) AS refs
        FOREACH (_ IN CASE WHEN refs = 0 THEN [1] ELSE [] END | DETACH DELETE v)
        RETURN 1 AS ok
        """
        res = self.db.run(cypher, {"entity": entity, "relation": relation, "key": key})
        return "Deleted (if it existed)."
