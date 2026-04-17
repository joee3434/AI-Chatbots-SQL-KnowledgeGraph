import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import json
from pathlib import Path
from kg_bot.graph_store import GraphStore


def run_kg_eval():
    store = GraphStore()

    with open(Path("evaluation/test_cases.json"), "r", encoding="utf-8") as f:
        cases = json.load(f)["kg_bot"]

    passed = 0
    total = len(cases)

    for case in cases:
        message = case["message"]
        parts = message.split()
        cmd = parts[0].lower()

        if cmd == "add" and len(parts) >= 4:
            entity = parts[1]
            relation = parts[2]
            value = " ".join(parts[3:])
            answer = store.add_fact(entity, relation, value)
        elif cmd == "inquire":
            if len(parts) == 1:
                answer = store.inquire()
            elif len(parts) == 2:
                answer = store.inquire(entity=parts[1])
            else:
                answer = store.inquire(entity=parts[1], relation=parts[2])
        else:
            answer = "Unsupported test command"

        ok = case["expected_answer_contains"].lower() in answer.lower()
        if ok:
            passed += 1

        print("=" * 60)
        print("Message:", message)
        print("Answer:", answer)
        print("Check:", ok)

    print("=" * 60)
    print(f"KG Evaluation Result: {passed}/{total} passed")

    store.close()


if __name__ == "__main__":
    run_kg_eval()
