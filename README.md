# AI Chatbots Platform

## Overview
This project implements two AI-powered chatbot systems:

- SQL-based chatbot (Inventory system)
- Knowledge Graph chatbot (Neo4j)

Extended with:
- Memory (short-term + long-term)
- FastAPI backend
- Evaluation framework

---

## Setup

### Clone project
```bash
git clone <YOUR_REPO_URL>
cd mid_project_chatbots
cat > README.md <<'EOF'
# AI Chatbots Platform

## Overview
This project implements two AI-powered chatbot systems:

- SQL-based chatbot (Inventory system)
- Knowledge Graph chatbot (Neo4j)

Extended with:
- Memory (short-term + long-term)
- FastAPI backend
- Evaluation framework

---

## Setup

### Clone project
```bash
git clone <YOUR_REPO_URL>
cd mid_project_chatbots
pip install -r requirements.txt
python3 -m sql_bot.app
show me assets in cairo
and what about alexandria?
show me assets in cairo
and what about alexandria?
add Egypt capital Cairo
inquire Egypt
uvicorn api.main:app --reload
uvicorn api.main:app --reload
python3 -m evaluation.sql_eval
python3 -m evaluation.sql_eval
Memory
Short-term: session-based
Long-term: stored in SQLite
Technologies
Python
SQLite
Neo4j
LangChain
LangGraph
Ollama
FastAPI
Uvicorn
Pydantic
Docker
Final Result

A complete AI system integrating:

LLM reasoning
SQL databases
Graph databases
Memory
API
Evaluation

