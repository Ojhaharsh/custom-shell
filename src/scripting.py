"""
Scripting / Pipelines
"""

import google.generativeai as genai
import os

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def generate_script(nl_input):
    """
    Generate multi-step script from NL
    """
    try:
        prompt = f"""
        Generate a bash script for the following natural language description:
        {nl_input}

        Output the script as a string, with proper error handling.
        """
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        script = response.text.strip()
        return script
    except:
        return f"#!/bin/bash\necho 'Generated script for {nl_input}'"

def augment_script(script, action):
    """
    Augment script: refactor, add error handling, test stubs
    """
    try:
        if action == 'refactor':
            prompt = f"Refactor this script for better readability:\n{script}"
        elif action == 'error_handling':
            prompt = f"Add error handling to this script:\n{script}"
        elif action == 'test_stubs':
            prompt = f"Add test stubs for this script:\n{script}"
        else:
            return script

        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text.strip()
    except:
        return script

def save_script(script, filename):
    with open(filename, 'w') as f:
        f.write(script)
    print(f"Script saved to {filename}")