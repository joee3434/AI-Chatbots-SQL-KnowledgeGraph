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
Create environment
python3 -m venv .venv
source .venv/bin/activate
Install dependencies
pip install -r requirements.txt
Run SQL Bot
python3 -m sql_bot.app

Example:

show me assets in cairo
and what about alexandria?
Run KG Bot
docker start neo4j
python3 -m kg_bot.main

Example:

add Egypt capital Cairo
inquire Egypt
Run API
uvicorn api.main:app --reload

Open:

http://127.0.0.1:8000/docs
API Endpoints
POST /sql-chat
POST /kg-chat
GET /history/{session_id}
Evaluation

Run SQL tests:

python3 -m evaluation.sql_eval

Run KG tests:

python3 -m evaluation.kg_eval
Memory
Short-term: session-based
Long-term: stored in SQLite
Technologies
Python
SQLite
Neo4j
LangChain / LangGraph
Ollama
FastAPI
Final Result

A complete AI system integrating:

LLM reasoning
SQL databases
Graph databases
Memory
API
Evaluation

