# Technical Notes

## 1. System Architecture

The project consists of two main chatbot modules:

### SQL Bot
Pipeline:
1. User question
2. LangGraph workflow
3. SQL generation
4. SQL validation
5. SQL execution on SQLite
6. Natural language response

Workflow nodes:
- Generator
- Executor
- Corrector
- Responder

### KG Bot
Pipeline:
1. User command
2. Intent parsing
3. Command decomposition
4. Cypher execution on Neo4j
5. Natural language response

Supported operations:
- add
- inquire
- update
- delete

---

## 2. Memory Architecture

### Short-Term Memory
Implemented in 
