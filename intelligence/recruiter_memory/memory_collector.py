# intelligence/recruiter_memory/memory_collector.py

from typing import Dict, List, Any
import time

class MemoryCollector:
    def __init__(self):
        self.logs: List[Dict[str, Any]] = []

    def record_activity(
        self,
        recruiter_id: str,
        candidate_id: str,
        action: str,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Logs a recruiter interaction with a candidate.
        Actions: viewed, saved, shortlisted, interviewed, hired, rejected.
        """
        log_entry = {
            "recruiter_id": recruiter_id,
            "candidate_id": candidate_id,
            "action": action.lower(),
            "timestamp": time.time(),
            "metadata": metadata or {}
        }
        self.logs.append(log_entry)
        return log_entry

    def get_recruiter_logs(self, recruiter_id: str) -> List[Dict[str, Any]]:
        return [log for log in self.logs if log["recruiter_id"] == recruiter_id]
