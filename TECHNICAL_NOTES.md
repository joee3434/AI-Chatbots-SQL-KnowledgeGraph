# Technical Notes – AI-Powered Chatbots

## 1. Design Philosophy

This project was designed following a modular, graph-based AI architecture.

Instead of implementing a simple linear pipeline, the system uses:

- LangChain for LLM interaction and prompt management
- LangGraph for structured state-machine execution
- Separation of concerns between generation, execution, correction, and response

This ensures scalability, clarity, and robustness.

---

# 2. Why LangGraph?

A traditional chain-based approach would look like:

User → Generate SQL → Execute → Respond

However, this approach lacks:

- Retry logic
- Conditional branching
- Error handling loops
- Explicit state management

LangGraph enables:

- Multi-step reasoning
- Conditional routing
- Automatic SQL correction loop
- Clear node-based architecture

Implemented nodes:

- Generator Node
- Executor Node
- Corrector Node
- Responder Node
- Give-up Node

---

# 3. Self-Correction Mechanism

If a generated SQL query fails:

1. The error is captured.
2. The system routes execution to the Corrector Node.
3. The LLM receives:
   - Original question
   - Failed SQL query
   - Execution error
4. A corrected SQL query is generated.
5. Execution is retried.

This loop runs up to a defined attempt limit.

This mimics production-grade AI retry strategies.

---

# 4. Business Rule Enforcement

The system enforces default business logic:

- Only active records are returned
- Assets with status Disposed or Retired are excluded

Unless the user explicitly requests otherwise.

The enforcement logic:

- Detects whether a WHERE clause already exists
- Appends conditions using AND
- Avoids duplicate WHERE errors

This ensures query safety and correctness.

---

# 5. SQL Security Considerations

The system prevents unsafe operations:

- Only SELECT statements allowed
- INSERT / UPDATE / DELETE / DROP blocked
- Table whitelist validation
- SQL validation before execution

This reduces the risk of prompt-injection or unsafe query execution.

---

# 6. Knowledge Graph Design

The Neo4j chatbot follows a CRUD-based architecture.

Intent classification is handled before execution.

Supported intents:

- add
- inquire
- update
- delete

Each maps to structured Cypher queries.

This ensures:

- Clean separation of intent and execution
- Structured graph management
- Clear data model (Entity – Relationship – Value)

---

# 7. Why Ollama Instead of OpenAI?

The system uses Ollama for:

- Local execution
- No API key requirement
- Offline capability
- Cost-free development

The architecture remains compatible with OpenAI and can be switched easily.

---

# 8. Limitations

- LLM accuracy depends on prompt quality
- Complex multi-table analytical queries may require additional prompt tuning
- Neo4j chatbot currently uses rule-based intent classification
- No persistent conversation memory implemented

---

# 9. Future Improvements

- Add conversation memory
- Improve structured SQL output formatting
- Add logging and monitoring
- Add test suite for validation
- Implement hybrid LLM fallback (OpenAI + Ollama)
- Add structured output parsing for safer SQL extraction

---

# 10. Engineering Summary

This project demonstrates:

- AI-driven database interaction
- Graph-based orchestration
- Structured error recovery
- Secure query validation
- Modular architecture
- Real-world AI system design principles

The architecture is scalable, production-oriented, and extensible.
