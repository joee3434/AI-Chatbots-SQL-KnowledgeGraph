from neo4j_client import Neo4jClient

def main():
    db = Neo4jClient("bolt://localhost:7687", "neo4j", "password123")
    try:
        res = db.run("RETURN 1 AS ok")
        print(res)
    finally:
        db.close()

if __name__ == "__main__":
    main()
