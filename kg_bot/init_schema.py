from neo4j_client import Neo4jClient

def main():
    db = Neo4jClient("bolt://localhost:7687", "neo4j", "password123")
    try:
        db.run("CREATE CONSTRAINT entity_name IF NOT EXISTS FOR (e:Entity) REQUIRE e.name IS UNIQUE;")
        db.run("CREATE CONSTRAINT value_key IF NOT EXISTS FOR (v:Value) REQUIRE v.key IS UNIQUE;")
        print("Neo4j schema initialized (constraints created).")
    finally:
        db.close()

if __name__ == "__main__":
    main()
