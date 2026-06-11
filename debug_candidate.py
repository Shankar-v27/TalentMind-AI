from preprocessing.parser import load_candidates
from config.settings import Settings
import json

candidates = load_candidates(
    Settings.CANDIDATE_FILE
)

print("Keys:")
print(candidates[0].keys())

print("\nFirst Candidate:")
print(
    json.dumps(
        candidates[0],
        indent=2
    )[:5000]
)
print("\nRedrob Signals:")
print(
    json.dumps(
        candidates[0]["redrob_signals"],
        indent=2
    )
)