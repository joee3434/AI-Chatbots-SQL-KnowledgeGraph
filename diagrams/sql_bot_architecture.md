# Inventory Chatbot Architecture (SQL + LangGraph)

```mermaid
flowchart TD

    A[User Input - Terminal CLI] --> B[Chitchat Detection]

    B -->|Greeting| C[Simple Conversational Response]
    B -->|Inventory Question| D[LangGraph State Machine]

    D --> E[Generator Node]
    E -->|LLM via LangChain (ChatOllama)| F[Generated SQL]

    F --> G[Executor Node]
    G --> H[SQL Validation + Business Rules]
    H --> I[SQLite Database Execution]

    I -->|Success| J[Responder Node]
    I -->|Error| K[Corrector Node]

    K -->|Fix SQL via LLM| G

    J --> L[Natural Language Answer]
    L --> M[Return to Terminal]



