from memory.short_term import ShortTermMemory
from memory.long_term import LongTermMemory


class MemoryManager:
    def __init__(self, short_term_limit=5):
        self.short_term = ShortTermMemory(max_history=short_term_limit)
        self.long_term = LongTermMemory()

    def add_message(self, session_id, role, content):
        self.short_term.add_message(session_id, role, content)
        self.long_term.add_message(session_id, role, content)

    def get_short_history(self, session_id):
        return self.short_term.get_history(session_id)

    def get_long_history(self, session_id, limit=10):
        return self.long_term.get_history(session_id, limit=limit)

    def clear_session(self, session_id):
        self.short_term.clear(session_id)
        self.long_term.clear_session(session_id)
