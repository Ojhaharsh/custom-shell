"""
Context & Memory
"""

import os

_context = {
    'cwd': os.getcwd(),
    'env': dict(os.environ),
    'history': [],
    'variables': {}
}

def get_context():
    return _context

def update_context(context, result):
    context['history'].append(result)
    # Update cwd if cd command
    if 'cd' in result.get('command', ''):
        # Parse cd command
        parts = result['command'].split()
        if len(parts) > 1:
            new_dir = parts[1]
            if os.path.isdir(new_dir):
                os.chdir(new_dir)
                context['cwd'] = os.getcwd()