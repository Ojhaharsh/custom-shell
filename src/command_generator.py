"""
Command Generator: Convert intent to shell command
"""

import google.generativeai as genai
import os
import platform

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def get_os_command(base_cmd):
    """Map Unix commands to Windows equivalents if on Windows"""
    if platform.system() == 'Windows':
        cmd_map = {
            'ls': 'dir',
            'cp': 'copy',
            'mv': 'move',
            'rm': 'del',
            'mkdir': 'mkdir',
            'rmdir': 'rmdir',
            'cat': 'type',
            'grep': 'findstr',
            'which': 'where',
            'pwd': 'cd',
            'ps': 'tasklist',
            'kill': 'taskkill /PID',
            'chmod': 'attrib',  # approximate
            'touch': 'echo. >',  # create empty file
            'find': 'dir /s /b',  # approximate
        }
        return cmd_map.get(base_cmd, base_cmd)
    return base_cmd

def generate_command(intent):
    """
    Generate shell command from intent
    """
    action = intent.get('action', '')
    if action == 'find':
        type_ = intent.get('type', '*')
        time_ = intent.get('time', '')
        dest = intent.get('dest', '/tmp')
        mtime = '-mtime -1' if time_ == 'recent' else ''
        if platform.system() == 'Windows':
            cmd = f'dir /s /b *.{type_}'  # Windows find equivalent
            if dest != '/tmp':
                cmd += f' | for %i in (*) do copy "%i" "{dest}"'  # rough copy
        else:
            cmd = f"find . -name '*.{type_}' {mtime} -exec cp {{}} {dest} \\;"
        return cmd
    elif action == 'list':
        path = intent.get('path', '.')
        cmd = get_os_command('ls') if platform.system() != 'Windows' else 'dir'
        return f"{cmd} {path}"
    elif action == 'change_dir':
        path = intent.get('path', '.')
        cmd = get_os_command('cd')
        return f"{cmd} {path}"
    elif action == 'clipboard_read':
        if platform.system() == 'Windows':
            return 'powershell -command "Get-Clipboard"'
        elif platform.system() == 'Darwin':  # macOS
            return 'pbpaste'
        else:  # Linux
            return 'xclip -selection clipboard -o'
    elif action == 'clipboard_write':
        content = intent.get('content', '')
        if platform.system() == 'Windows':
            return f'powershell -command "Set-Clipboard -Value \\"{content}\\""'
        elif platform.system() == 'Darwin':  # macOS
            return f'echo "{content}" | pbcopy'
        else:  # Linux
            return f'echo "{content}" | xclip -selection clipboard'
    elif action == 'copy':
        src = intent.get('src', '')
        dest = intent.get('dest', '')
        cmd = get_os_command('cp')
        return f"{cmd} {src} {dest}"
    elif action == 'move':
        src = intent.get('src', '')
        dest = intent.get('dest', '')
        cmd = get_os_command('mv')
        return f"{cmd} {src} {dest}"
    elif action == 'delete':
        target = intent.get('target', '')
        cmd = get_os_command('rm')
        return f"{cmd} {target}"
    else:
        try:
            # LLM fallback
            prompt = f"Generate a shell command for intent: {intent}. Use {platform.system()} commands."
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            return response.text.strip()
        except:
            return f"echo 'Unknown command for {intent}'"