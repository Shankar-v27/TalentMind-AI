#!/usr/bin/env python3
"""
Fix corrupted candidates.jsonl file by removing invalid JSON lines.
"""

import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

INPUT_FILE = "data/candidates.jsonl"
OUTPUT_FILE = "data/candidates_fixed.jsonl"
BACKUP_FILE = "data/candidates_backup.jsonl"

def fix_candidates_jsonl():
    """Remove corrupted JSON lines from candidates.jsonl"""
    
    valid_count = 0
    invalid_count = 0
    invalid_lines = []
    
    logger.info(f"Reading from {INPUT_FILE}...")
    
    try:
        # Read all lines
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        logger.info(f"Total lines: {len(lines)}")
        
        # Write valid JSON lines to output file
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as out_f:
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                if not line:
                    continue
                    
                try:
                    # Validate JSON
                    json.loads(line)
                    out_f.write(line + '\n')
                    valid_count += 1
                except json.JSONDecodeError as e:
                    invalid_count += 1
                    invalid_lines.append((line_num, str(e)[:100]))
                    if invalid_count <= 5:  # Log first 5 errors
                        logger.warning(f"Line {line_num} invalid: {str(e)[:100]}")
        
        logger.info(f"Valid lines: {valid_count}")
        logger.info(f"Invalid lines: {invalid_count}")
        
        if invalid_lines:
            logger.info(f"First 5 invalid lines:")
            for line_num, error in invalid_lines[:5]:
                logger.info(f"  Line {line_num}: {error}")
        
        # Backup original and replace
        import shutil
        logger.info(f"Backing up original to {BACKUP_FILE}...")
        shutil.copy(INPUT_FILE, BACKUP_FILE)
        
        logger.info(f"Replacing {INPUT_FILE} with cleaned version...")
        shutil.move(OUTPUT_FILE, INPUT_FILE)
        
        logger.info("✓ Successfully fixed candidates.jsonl")
        return True
        
    except Exception as e:
        logger.error(f"Error fixing file: {str(e)}", exc_info=True)
        return False

if __name__ == "__main__":
    fix_candidates_jsonl()
