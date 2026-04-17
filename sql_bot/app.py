from .state_graph import build_graph
from memory.memory_manager import MemoryManager


def is_chitchat(text: str) -> bool:
    t = text.strip().lower()
    greetings = {"hi", "hello", "hey", "how are you", "good morning", "good evening"}
    return t in greetings or t.startswith("hi ") or t.startswith("hello ") or t.startswith("hey ")


def main():
    print("Inventory Chatbot (SQL) - CLI")
    print("Type 'exit' to quit.\n")

    graph = build_graph()
    memory = MemoryManager()
    session_id = "sql_demo_session"

    while True:
        q = input("You: ").strip()
        if not q:
            continue

        if q.lower() in {"exit", "quit"}:
            print("Bot: Goodbye.")
            break

        # save user message to memory
        memory.add_message(session_id, "user", q)

        if is_chitchat(q):
            answer = "Hello! Ask me about assets, vendors, inventory levels, or locations."
            print("Bot:", answer)
            memory.add_message(session_id, "assistant", answer)
            continue

        history = memory.get_short_history(session_id)
        state = {"question": q, "attempts": 0, "history": history}
        out = graph.invoke(state)

        sql_text = out.get("sql", "")
        answer = out.get("answer", "No answer.")

        print("SQL:", sql_text)
        print("Bot:", answer)

        # save bot response to memory
        memory.add_message(session_id, "assistant", answer)


if __name__ == "__main__":
    main()
