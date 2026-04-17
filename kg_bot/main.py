from .graph_store import GraphStore

def classify_intent(text: str) -> str:
    t = text.strip().lower()
    if t.startswith("add "):
        return "add"
    if t.startswith("delete ") or t.startswith("remove "):
        return "delete"
    if t.startswith("update ") or t.startswith("edit "):
        return "update"
    return "inquire"

def parse_simple_fact(text: str):
    # Expected formats:
    # add <entity> <relation> <value...>
    # update <entity> <relation> <new_value...>
    # delete <entity> <relation>
    parts = text.strip().split()
    cmd = parts[0].lower()
    if cmd in {"add", "update"} and len(parts) >= 4:
        entity = parts[1]
        relation = parts[2]
        value = " ".join(parts[3:])
        return cmd, entity, relation, value
    if cmd in {"delete", "remove"} and len(parts) >= 3:
        entity = parts[1]
        relation = parts[2]
        return "delete", entity, relation, None
    return None

def main():
    print("Knowledge Graph Chatbot (Neo4j) - CLI")
    print("Commands:")
    print("  add <entity> <relation> <value>")
    print("  update <entity> <relation> <new_value>")
    print("  delete <entity> <relation>")
    print("  inquire <entity> (optional)")
    print("Type 'exit' to quit.\n")

    store = GraphStore()
    try:
        while True:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in {"exit", "quit"}:
                print("Bot: Goodbye.")
                break

            intent = classify_intent(user_input)
            parsed = parse_simple_fact(user_input)

            if intent in {"add", "update", "delete"}:
                if not parsed:
                    print("Bot: Invalid format. Try: add <entity> <relation> <value>")
                    continue

                cmd, entity, relation, value = parsed
                if cmd == "add":
                    print("Bot:", store.add_fact(entity, relation, value))
                elif cmd == "update":
                    print("Bot:", store.update_fact(entity, relation, value))
                else:
                    print("Bot:", store.delete_fact(entity, relation))

            else:
                # inquire
                parts = user_input.split()
                if len(parts) == 1:
                    # show all
                    print("Bot:\n" + store.inquire())
                elif len(parts) == 2 and parts[0].lower() == "inquire":
                    print("Bot:\n" + store.inquire(entity=parts[1]))
                elif len(parts) == 3 and parts[0].lower() == "inquire":
                    print("Bot:\n" + store.inquire(entity=parts[1], relation=parts[2]))
                else:
                    # treat as inquire all for now
                    print("Bot:\n" + store.inquire())

    finally:
        store.close()

if __name__ == "__main__":
    main()
