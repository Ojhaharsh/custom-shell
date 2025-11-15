"""
Executor: Sandboxed execution
"""

import subprocess
import os

from src.audit import log_command

def execute_command(command, context, dry_run=False):
    """
    Execute command in controlled environment
    """
    if dry_run:
        return {'output': f"Dry-run: {command}", 'success': True}

    try:
        # Run with timeout
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=context.get('cwd', os.getcwd()), timeout=30)
        output = result.stdout + result.stderr
        return {'output': output, 'success': result.returncode == 0, 'command': command}
    except subprocess.TimeoutExpired:
        result = {'output': 'Command timed out', 'success': False, 'command': command}
        log_command(command, result)
        return result
    except Exception as e:
        result = {'output': str(e), 'success': False, 'command': command}
        log_command(command, result)
        return result

    log_command(command, {'output': output, 'success': result.returncode == 0, 'command': command})
    return {'output': output, 'success': result.returncode == 0, 'command': command}