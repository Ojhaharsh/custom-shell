"""
Frontend REPL for the Custom Shell
"""

import os
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style

from src.scripting import generate_script, augment_script, save_script
from src.intent_parser import parse_intent
from src.command_generator import generate_command
from src.planner import plan_command
from src.executor import execute_command
from src.context import get_context, update_context

# Style for the prompt
style = Style.from_dict({
    'prompt': 'ansicyan bold',
})

# Completer for basic commands
completer = WordCompleter(['help', 'exit', 'explain', 'preview', 'run', 'dry-run'], ignore_case=True)

def start_repl():
    # Prompt for API key if not set
    if not os.getenv('GEMINI_API_KEY'):
        api_key = input("Enter your Gemini API key: ")
        os.environ['GEMINI_API_KEY'] = api_key
        # Reconfigure genai
        import google.generativeai as genai
        genai.configure(api_key=api_key)

    session = PromptSession(completer=completer, style=style)
    context = get_context()

    while True:
        try:
            user_input = session.prompt(f"{os.getcwd()}> ").strip()
            if not user_input:
                continue
            if user_input.lower() in ['exit', 'quit']:
                break
            if user_input.lower() == 'help':
                print("Type natural language commands or shell commands. Use 'explain' for explanations, 'preview' for dry-run, 'run' to execute.")
                print("Use 'script <description>' to generate a script, 'augment <action> <script>' to modify.")
                continue

            if user_input.startswith('script '):
                desc = user_input[7:]
                script = generate_script(desc)
                print(f"Generated script:\n{script}")
                save_name = input("Save as (filename.sh): ")
                if save_name:
                    save_script(script, save_name)
                continue

            if user_input.startswith('augment '):
                parts = user_input.split(' ', 2)
                if len(parts) < 3:
                    print("Usage: augment <action> <script>")
                    continue
                action, script_content = parts[1], parts[2]
                augmented = augment_script(script_content, action)
                print(f"Augmented script:\n{augmented}")
                continue

            # Determine if NL or shell
            if user_input.startswith('!'):  # Force shell command
                command = user_input[1:]
                intent = None
            else:
                # Assume NL
                intent = parse_intent(user_input, context)
                command = generate_command(intent)

            # Plan and safety
            plan = plan_command(command, context)
            if not plan['safe']:
                print(f"Unsafe command: {plan['reason']}")
                continue

            # Show explanation
            if intent:
                print(f"Intent: {intent}")
            print(f"Plan: {plan['explanation']}")
            if plan['affected_files']:
                print(f"Affected files: {plan['affected_files']}")

            # Ask for confirmation
            confirm = input(f"Execute: {command}? (y/n/preview/dry-run): ").lower()
            if confirm == 'n':
                continue
            elif confirm == 'preview' or confirm == 'dry-run':
                result = execute_command(command, context, dry_run=True)
                print(result['output'])
                continue

            # Execute
            result = execute_command(command, context)
            print(result['output'])
            update_context(context, result)

        except KeyboardInterrupt:
            continue
        except EOFError:
            break

    print("Goodbye!")