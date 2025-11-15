"""
Planner & Safety Layer
"""

import os

def plan_command(command, context):
    """
    Produce safe plan
    """
    plan = {
        'safe': True,
        'reason': '',
        'dry_run': f"echo 'Would run: {command}'",
        'affected_files': [],
        'explanation': f"Command: {command}"
    }

    # Safety checks
    dangerous_patterns = [
        'rm -rf /',
        'rm -rf /*',
        'dd if=',
        'mkfs',
        'format',
        '> /dev/',
        'chmod 777 /'
    ]
    for pattern in dangerous_patterns:
        if pattern in command:
            plan['safe'] = False
            plan['reason'] = f"Potentially destructive operation: {pattern}"

    # Parse affected files (simple)
    if 'cp' in command or 'mv' in command:
        parts = command.split()
        for part in parts:
            if os.path.exists(part):
                plan['affected_files'].append(part)

    return plan