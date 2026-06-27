# memory/debate_memory.py

from typing import Dict, List, Any

class DebateMemory:
    def __init__(self):
        self._history = {}

    def save(self, candidate_id: str, debate_data: Dict[str, Any]):
        """
        Store debate outputs in active memory.
        """
        self._history[candidate_id] = debate_data

    def retrieve(self, candidate_id: str) -> Dict[str, Any]:
        """
        Get debate details from memory.
        """
        return self._history.get(candidate_id, {})
