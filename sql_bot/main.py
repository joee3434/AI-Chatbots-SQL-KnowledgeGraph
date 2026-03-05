def is_chitchat(text: str) -> bool:
    t = text.strip().lower()
    greetings = {"hi", "hello", "hey", "how are you", "good morning", "good evening"}
    return t in greetings or t.startswith("hi ") or t.startswith("hello ") or t.startswith("hey ")

def main():
    print("Inventory Chatbot (SQL) - CLI")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            print("Bot: Goodbye.")
            break

        if is_chitchat(user_input):
            print("Bot: Hello! Ask me about inventory, assets, vendors, or locations.")
            continue

        print("Bot: (placeholder) I received your query. Next step: generate SQL and execute it.")

if __name__ == "__main__":
    main()
