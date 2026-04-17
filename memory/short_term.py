class ShortTermMemory:
    def __init__(self, max_history=5):
        self.max_history = max_history
        self.sessions = {}

    def add_message(self, session_id, role, content):
        if session_id not in self.sessions:
            self.sessions[session_id] = []

        self.sessions[session_id].append({
            "role": role,
            "content": content
        })

        # keep only last N messages
        if len(self.sessions[session_id]) > self.max_history:
            self.sessions[session_id] = self.sessions[session_id][-self.max_history:]

    def get_history(self, session_id):
        return self.sessions.get(session_id, [])

    def clear(self, session_id):
        if session_id in self.sessions:
            del self.sessions[session_id]
