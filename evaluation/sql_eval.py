import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import json
from pathlib import Path
from sql_bot.state_graph import build_graph


def run_sql_eval():
    graph = build_graph()

    with open(Path("evaluation/test_cases.json"), "r", encoding="utf-8") as f:
        cases = json.load(f)["sql_bot"]

    passed = 0
    total = len(cases)

    for case in cases:
        state = {
            "question": case["question"],
            "attempts": 0,
            "history": []
        }

        out = graph.invoke(state)

        sql_text = out.get("sql", "")
        answer = out.get("answer", "")

        sql_ok = case["expected_sql_contains"] in sql_text
        answer_ok = case["expected_answer_contains"].lower() in answer.lower()

        if sql_ok and answer_ok:
            passed += 1

        print("=" * 60)
        print("Question:", case["question"])
        print("Generated SQL:", sql_text)
        print("Answer:", answer)
        print("SQL Check:", sql_ok)
        print("Answer Check:", answer_ok)

    print("=" * 60)
    print(f"SQL Evaluation Result: {passed}/{total} passed")


if __name__ == "__main__":
    run_sql_eval()
