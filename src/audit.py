"""
Explainability & Audit
"""

import logging

logging.basicConfig(filename='audit.log', level=logging.INFO)

def log_action(action, details):
    logging.info(f"{action}: {details}")

def log_command(command, result):
    log_action('execute', f"Command: {command}, Success: {result['success']}, Output: {result['output'][:100]}...")