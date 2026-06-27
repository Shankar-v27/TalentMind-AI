# intelligence/career_forecasting/career_simulator.py

from typing import Dict, Any

class CareerSimulator:
    def simulate(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Simulate progress branches under diverse corporate environments.
        """
        dna = candidate.get("candidate_dna", {})
        learning = float(dna.get("learning", 0.75) or 0.75)
        
        startup_years = max(1, int(round(3.0 - learning * 1.5)))
        corp_years = max(2, int(round(6.0 - learning * 2.0)))
        faang_years = max(2, int(round(5.0 - learning * 1.5)))
        
        return {
            "startup": {
                "years": startup_years,
                "role": "Engineering Manager",
                "milestone": f"Attain manager status in {startup_years} years due to fast pacing."
            },
            "corporate": {
                "years": corp_years,
                "role": "Manager",
                "milestone": f"Attain structured Manager role in {corp_years} years."
            },
            "faang": {
                "years": faang_years,
                "role": "Staff Engineer",
                "milestone": f"Attain Staff Engineer level in {faang_years} years."
            }
        }
