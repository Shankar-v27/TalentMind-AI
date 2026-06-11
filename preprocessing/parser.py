# preprocessing/parser.py

import jsonlines
from tqdm import tqdm


def load_candidates(file_path):
    """
    Load candidates.jsonl
    Returns a list of dictionaries
    """

    candidates = []

    with jsonlines.open(file_path) as reader:

        for candidate in tqdm(
            reader,
            desc="Loading Candidates"
        ):

            candidates.append(candidate)


    print(
        f"Loaded {len(candidates)} candidates"
    )

    return candidates