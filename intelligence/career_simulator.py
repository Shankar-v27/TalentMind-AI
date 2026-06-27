# intelligence/career_simulator.py

from typing import Dict, Any

class CareerSimulator:
    ROLE_HIERARCHY = {
        "intern": 0,
        "junior": 1,
        "engineer": 2,
        "developer": 2,
        "specialist": 2,
        "senior": 3,
        "lead": 4,
        "principal": 4,
        "manager": 5,
        "director": 6,
        "vp": 7,
        "cto": 8,
        "founder": 8,
        "ceo": 8
    }

    def _get_role_level(self, title: str) -> int:
        title = title.lower()
        # Find the highest matched level
        best_level = 2  # Default to mid-level engineer
        for role, level in self.ROLE_HIERARCHY.items():
            if role in title:
                best_level = max(best_level, level) if best_level != 2 else level
        return best_level

    def simulate(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """
        Converts job titles into hierarchy levels and simulates career acceleration,
        momentum, and promotion probabilities.
        """
        career = candidate.get("career_history", [])
        
        # Extract title hierarchy levels (career history is ordered from most recent to oldest)
        levels = [self._get_role_level(job.get("title", "")) for job in career]
        
        if not levels:
            headline = candidate.get("profile", {}).get("headline", "")
            levels = [self._get_role_level(headline)]
            
        current_level = levels[0] if levels else 2
        start_level = levels[-1] if levels else 2
        level_delta = current_level - start_level
        
        # Calculate career velocity features
        num_jobs = len(career) if career else 1
        promotion_freq = max(0.0, level_delta) / max(1.0, num_jobs)
        
        # Career acceleration computation
        raw_acc = 0.3 + (promotion_freq * 0.4) + (level_delta * 0.1)
        # Give a small bonus for fewer jobs on higher levels (indicates faster progression)
        if current_level >= 3:
            raw_acc += 0.1
        career_acceleration = round(min(0.98, max(0.1, raw_acc)), 2)
        career_momentum = round(min(0.99, max(0.15, career_acceleration * 1.1)), 2)
        
        # Determine Growth Speed
        if career_acceleration >= 0.70:
            growth_speed = "FAST"
        elif career_acceleration >= 0.45:
            growth_speed = "STEADY"
        else:
            growth_speed = "CONVENTIONAL"
            
        # Predict Future Role based on current level
        predicted_level = min(8, current_level + 1)
        level_to_role = {
            0: "Junior Engineer",
            1: "Engineer",
            2: "Senior Engineer",
            3: "Tech Lead",
            4: "Engineering Manager",
            5: "Director of Engineering",
            6: "VP of Engineering",
            7: "CTO",
            8: "CTO"
        }
        predicted_role = level_to_role.get(predicted_level, "Senior Engineer")
        
        # Promotion Probability
        promotion_prob = round(min(0.99, max(0.1, 0.35 + (career_acceleration * 0.5) + (current_level * 0.02))), 2)
        
        return {
            "career_acceleration": career_acceleration,
            "career_momentum": career_momentum,
            "growth_speed": growth_speed,
            "predicted_role": predicted_role,
            "promotion_probability": promotion_prob,
            "current_level": current_level
        }
