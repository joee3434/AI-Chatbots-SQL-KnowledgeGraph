from .state_graph import build_graph

def is_chitchat(text: str) -> bool:
    t = text.strip().lower()
    greetings = {"hi", "hello", "hey", "how are you", "good morning", "good evening"}
    return t in greetings or t.startswith("hi ") or t.startswith("hello ") or t.startswith("hey ")

def main():
    print("Inventory Chatbot (SQL) - CLI")
    print("Type 'exit' to quit.\n")

    graph = build_graph()

    while True:
        q = input("You: ").strip()
        if not q:
            continue
        if q.lower() in {"exit", "quit"}:
            print("Bot: Goodbye.")
            break

        if is_chitchat(q):
            print("Bot: Hello! Ask me about assets, vendors, inventory levels, or locations.")
            continue

        state = {"question": q, "attempts": 0}
        out = graph.invoke(state)

        # Present Query (for debugging and assignment requirements)
        print("SQL:", out.get("sql", ""))

        print("Bot:", out.get("answer", "No answer."))

if __name__ == "__main__":
    main()
