# intelligence/future_simulator.py

from typing import Dict, Any

class FutureSimulator:
    def simulate(self, career_sim: Dict[str, Any], promotion_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Projects job title promotions across Year 0 (2026) to Year 5 (2031) based on
        current hierarchy levels and career momentum indicators.
        """
        current_level = career_sim.get("current_level", 2)
        promo_prob = promotion_data.get("promotion_probability", 0.5)
        
        # Establish cadence (in years) required for promotion steps
        if promo_prob >= 0.78:
            years_per_promo = 1
        elif promo_prob >= 0.50:
            years_per_promo = 2
        else:
            years_per_promo = 3
            
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
        
        base_year = 2026
        timeline = {}
        
        # Year 0 (2026)
        timeline[str(base_year)] = level_to_role.get(current_level, "Senior Engineer")
        
        # Year 1 (2027)
        lvl_1 = min(8, current_level + (1 if years_per_promo == 1 else 0))
        timeline[str(base_year + 1)] = level_to_role.get(lvl_1, "Senior Engineer")
        
        # Year 2 (2028)
        lvl_2 = min(8, current_level + (2 if years_per_promo == 1 else 1))
        timeline[str(base_year + 2)] = level_to_role.get(lvl_2, "Senior Engineer")
        
        # Year 3 (2029)
        lvl_3 = min(8, current_level + (3 if years_per_promo == 1 else (2 if years_per_promo == 2 else 1)))
        timeline[str(base_year + 3)] = level_to_role.get(lvl_3, "Senior Engineer")
        
        # Year 5 (2031)
        lvl_5 = min(8, current_level + (5 if years_per_promo == 1 else (3 if years_per_promo == 2 else 2)))
        timeline[str(base_year + 5)] = level_to_role.get(lvl_5, "Senior Engineer")
        
        return timeline
