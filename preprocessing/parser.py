# preprocessing/parser.py

import jsonlines
import logging
from tqdm import tqdm

logger = logging.getLogger(__name__)


def load_candidates(file_path):
    """
    Load candidates.jsonl
    Returns a list of dictionaries
    Skips corrupted JSON lines with logging
    """

    candidates = []
    skipped_lines = []
    line_number = 0

    try:
        with jsonlines.open(file_path) as reader:

            for line_number, candidate in enumerate(reader, 1):
                try:
                    candidates.append(candidate)
                except Exception as e:
                    logger.warning(f"Skipping corrupted line {line_number}: {str(e)}")
                    skipped_lines.append((line_number, str(e)))
                    continue

    except Exception as e:
        logger.error(f"Error reading JSONL file: {str(e)}")
        # If we have at least some candidates, continue with what we have
        if candidates:
            logger.info(f"Continuing with {len(candidates)} valid candidates despite read errors")
        else:
            raise

    if skipped_lines:
        logger.info(f"Skipped {len(skipped_lines)} corrupted lines: {skipped_lines[:5]}")

    logger.info(f"Loaded {len(candidates)} valid candidates")

    return candidates