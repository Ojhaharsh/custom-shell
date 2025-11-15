"""
Intent Parser: Parse natural language to intent
"""

import os
import google.generativeai as genai
from src.context import get_context

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))  # Assume set

def parse_intent(nl_input, context):
    """
    Parse NL to canonical intent JSON
    """
    try:
        prompt = f"""
        Parse the natural language command to a JSON intent.
        Context: {context}
        Input: {nl_input}

        Output JSON with keys: action, target, params, etc.
        Example: {{"action": "find", "target": "files", "type": "jpeg", "time": "recent", "dest": "/tmp"}}
        """

        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        intent_str = response.text.strip()
        # Parse JSON
        import json
        try:
            intent = json.loads(intent_str)
        except:
            intent = {"action": "unknown", "input": nl_input}
        return intent
    except Exception as e:
        # Fallback: simple keyword matching
        nl_lower = nl_input.lower()
        if 'find' in nl_lower and ('copy' in nl_lower or 'move' in nl_lower):
            type_ = 'jpeg' if 'jpeg' in nl_lower else '*'
            dest = '/tmp'
            if 'copy' in nl_lower:
                action = 'find'
            else:
                action = 'find'  # could extend
            return {"action": "find", "type": type_, "time": "recent" if 'recent' in nl_lower else "", "dest": dest}
        elif any(word in nl_lower for word in ['list', 'show', 'display']):
            path = '.'
            if 'parent' in nl_lower:
                path = '..'
            return {"action": "list", "path": path}
        elif any(phrase in nl_lower for phrase in ['go to', 'change to', 'cd to', 'navigate to']):
            if 'parent' in nl_lower or '..' in nl_lower:
                path = '..'
            elif 'home' in nl_lower:
                path = '~'
            else:
                # Try to extract path
                words = nl_lower.split()
                for i, word in enumerate(words):
                    if word in ['to', 'directory']:
                        if i + 1 < len(words):
                            path = words[i + 1]
                            break
                else:
                    path = '.'
            return {"action": "change_dir", "path": path}
        elif 'clipboard' in nl_lower:
            if any(word in nl_lower for word in ['copy', 'get', 'read', 'show']):
                return {"action": "clipboard_read"}
            elif any(word in nl_lower for word in ['paste', 'write', 'set']):
                # Extract content to paste
                return {"action": "clipboard_write", "content": nl_input}
            else:
                return {"action": "clipboard_read"}
        else:
            return {"action": "unknown", "input": nl_input}