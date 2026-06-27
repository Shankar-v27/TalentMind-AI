# intelligence/time_machine/candidate_movement.py

from typing import Dict, List, Any

class CandidateMovementEngine:
    def calculate_movement(
        self,
        before_list: List[Dict[str, Any]],
        after_list: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Compares two ranked lists and tracks shifts in position.
        Returns a list of candidate movements.
        """
        # Create map of positions
        before_pos = {item["candidate_id"]: idx + 1 for idx, item in enumerate(before_list)}
        after_pos = {item["candidate_id"]: idx + 1 for idx, item in enumerate(after_list)}
        
        movements = []
        for item in after_list:
            c_id = item["candidate_id"]
            old_rank = before_pos.get(c_id, 999)
            new_rank = after_pos.get(c_id, 999)
            delta = old_rank - new_rank # positive = moved up, negative = moved down
            
            movements.append({
                "candidate_id": c_id,
                "name": item["name"],
                "old_rank": old_rank,
                "new_rank": new_rank,
                "delta": delta,
                "score": item["score"]
            })
            
        return movements
