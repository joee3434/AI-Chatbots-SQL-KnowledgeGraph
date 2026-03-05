# AI-Powered Chatbots (Mid-Project)

This project implements two terminal-based AI conversational agents:

1. Inventory Chatbot (SQL + LangGraph)
2. Knowledge Graph Chatbot (Neo4j)

Both applications run entirely in the terminal (CLI) and follow a structured AI-driven architecture.

---

# 1. Project Overview

This project demonstrates:

- Natural language to database query translation
- Graph-based state machine reasoning
- AI-driven SQL generation and correction
- Interactive knowledge graph management
- Clean software architecture using LangChain and LangGraph

---

# 2. Inventory Chatbot (SQL)

## Objective

Translate natural language questions into SQL queries, execute them against a relational database, and return natural language responses.

## Architecture

- LLM integration via LangChain (ChatOllama)
- State machine orchestration via LangGraph
- SQLite database backend
- Self-correction loop for SQL errors
- Business rule enforcement (Active records only by default)

## Execution Flow

User Input  
→ Generator Node (LLM creates SQL)  
→ Executor Node (Validate + Apply business rules + Execute SQL)  
→ If Error → Corrector Node (LLM fixes SQL)  
→ Responder Node (Natural language answer)  

---

## Business Rules

By default:
- Only Active records are returned
- Assets with status Disposed or Retired are excluded

Unless the user explicitly asks to include them.

---

# 3. Knowledge Graph Chatbot (Neo4j)

## Objective

Allow users to dynamically manage and query factual data using natural language.

## Supported Operations

- add <entity> <relation> <value>
- inquire <entity>
- update <entity> <relation> <new_value>
- delete <entity> <relation>

## Architecture

User Input  
→ Intent Classification  
→ Cypher Query Generation  
→ Neo4j Execution  
→ Natural Language Response  

---

# 4. Technologies Used

- Python 3.11+
- LangChain
- LangGraph
- Ollama (Local LLM)
- SQLite
- Neo4j
- Mermaid (Architecture Diagrams)

---

# 5. Setup Instructions (Ubuntu)

## 1️⃣ Clone Repository

```bash
git clone <your_repo_url>
cd mid_project_chatbots
2️⃣ Create Virtual Environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
3️⃣ Install Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3
4️⃣ Run SQL Bot
python3 -m sql_bot.app
5️⃣ Run Knowledge Graph Bot
python3 kg_bot/init_schema.py
python3 kg_bot/main.py
6. Example Usage
SQL Bot
You: how many assets do we have?
Bot: You have a total of 3 active assets.

You: show me assets in cairo
Bot: We have 2 assets located in Cairo...
Knowledge Graph Bot
You: add Egypt capital Cairo
Bot: Stored fact: Egypt capital Cairo.

You: inquire Egypt
Bot: Egypt capital Cairo
7. Project Structure
mid_project_chatbots/
│
├── sql_bot/
│   ├── app.py
│   ├── state_graph.py
│   ├── sql_guard.py
│   ├── prompts.py
│   └── db/
│
├── kg_bot/
│   ├── main.py
│   ├── graph_store.py
│   ├── neo4j_client.py
│   └── init_schema.py
│
├── diagrams/
│
├── TECHNICAL_NOTES.md
├── requirements.txt
└── README.md
8. Key Features

AI-generated SQL queries

Automatic SQL error correction

Business rule enforcement

Graph-based state machine

Fully CLI-based execution

Local LLM (No OpenAI API required)

9. Author

Mid-Project Submission
AI-Powered Conversational Agents
