# intelligence/organization_dna.py

from typing import Dict, Any

class OrganizationDNA:
    DNA_PROFILES = {
        "startup": {
            "speed": 0.95,
            "ownership": 0.97,
            "innovation": 0.96,
            "risk": 0.90,
            "hierarchy": 0.10,
            "documentation": 0.25,
            "leadership": 0.80,
            "communication": 0.70,
            "execution": 0.88,
            "adaptability": 0.98,
            "learning": 0.92,
            "experimentation": 0.95,
            "discipline": 0.60,
            "process": 0.20,
            "compliance": 0.30,
            "teamwork": 0.85,
            "collaboration": 0.90,
            "creativity": 0.95,
            "stability": 0.30,
            "ambiguity": 0.96,
            "customer": 0.85,
            "autonomy": 0.96,
            "decision_speed": 0.95,
            "accountability": 0.90
        },
        "corporate": {
            "speed": 0.70,
            "ownership": 0.65,
            "innovation": 0.55,
            "risk": 0.40,
            "hierarchy": 0.80,
            "documentation": 0.85,
            "leadership": 0.95,
            "communication": 0.95,
            "execution": 0.92,
            "adaptability": 0.60,
            "learning": 0.75,
            "experimentation": 0.45,
            "discipline": 0.85,
            "process": 0.90,
            "compliance": 0.80,
            "teamwork": 0.80,
            "collaboration": 0.85,
            "creativity": 0.50,
            "stability": 0.85,
            "ambiguity": 0.40,
            "customer": 0.90,
            "autonomy": 0.50,
            "decision_speed": 0.50,
            "accountability": 0.85
        },
        "government": {
            "speed": 0.20,
            "ownership": 0.40,
            "innovation": 0.10,
            "risk": 0.05,
            "hierarchy": 0.95,
            "documentation": 0.98,
            "leadership": 0.50,
            "communication": 0.60,
            "execution": 0.70,
            "adaptability": 0.30,
            "learning": 0.50,
            "experimentation": 0.10,
            "discipline": 0.95,
            "process": 0.98,
            "compliance": 0.99,
            "teamwork": 0.70,
            "collaboration": 0.75,
            "creativity": 0.20,
            "stability": 0.97,
            "ambiguity": 0.10,
            "customer": 0.70,
            "autonomy": 0.20,
            "decision_speed": 0.15,
            "accountability": 0.80
        }
    }

    def generate(self, company_type: str = "corporate", custom_dimensions: Dict[str, float] = None) -> Dict[str, float]:
        """
        Generates an organization's personality vector.
        """
        company_type = company_type.lower()
        base_dna = self.DNA_PROFILES.get(company_type, self.DNA_PROFILES["corporate"]).copy()
        if custom_dimensions:
            base_dna.update(custom_dimensions)
        return base_dna
        
    def match(self, candidate: Dict[str, Any], learning_velocity: float, career_sim: Dict[str, Any], target_dna_type: str = "corporate") -> Dict[str, Any]:
        """
        Preserves backward compatibility for other modules.
        """
        target_dna_type = target_dna_type.lower()
        if target_dna_type not in self.DNA_PROFILES:
            target_dna_type = "corporate"
            
        target_vector = self.DNA_PROFILES[target_dna_type]
        
        # simple match algorithm for backward compatibility
        keys = ["speed", "risk", "ownership", "innovation", "process", "stability"]
        candidate_vector = {
            "speed": learning_velocity,
            "risk": 1.0 - float(candidate.get("redrob_signals", {}).get("interview_completion_rate", 0.5)),
            "ownership": career_sim.get("career_acceleration", 0.5),
            "innovation": learning_velocity * 0.9,
            "process": 0.8 if any(edu.get("tier") == "tier_1" for edu in candidate.get("education", [])) else 0.5,
            "stability": float(candidate.get("redrob_signals", {}).get("offer_acceptance_rate", 0.5))
        }
        
        abs_diff_sum = sum(abs(candidate_vector[k] - target_vector.get(k, 0.5)) for k in keys)
        avg_diff = abs_diff_sum / len(keys)
        culture_fit = round(max(0.1, min(0.99, 1.0 - avg_diff)), 2)
        
        return {
            "culture_fit": culture_fit,
            "work_style": "Excellent" if culture_fit >= 0.8 else "Good",
            "candidate_dna": candidate_vector,
            "target_dna_type": target_dna_type.title()
        }
