
```markdown
# Knowledge Graph Chatbot Architecture (Neo4j)

```mermaid
flowchart TD

    A[User Input - Terminal CLI] --> B[Intent Classification]

    B -->|Add| C[Add Fact Node]
    B -->|Inquire| D[Query Fact Node]
    B -->|Update| E[Update Fact Node]
    B -->|Delete| F[Delete Fact Node]

    C --> G[Cypher Query Builder]
    D --> G
    E --> G
    F --> G

    G --> H[Neo4j Database Execution]

    H --> I[Result Processing]
    I --> J[Natural Language Response]
    J --> K[Return to Terminal]
