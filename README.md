# Custom Shell 🐚

An AI-powered interactive shell that understands natural language commands and executes them safely across Windows, Mac, and Linux.

## Features

- **Natural Language Processing** - Type commands in plain English: *"list files in current directory"*
- **Safe Execution** - Dry-run previews, confirmations, and automatic danger detection
- **AI Script Generation** - Generate multi-step scripts from descriptions
- **Script Augmentation** - Refactor, add error handling, or create test stubs using AI
- **Context & Memory** - Maintains session state, working directory, and command history
- **Audit Logging** - Tracks all commands and their results for compliance
- **Cross-Platform** - Works seamlessly on Windows, macOS, and Linux

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/custom-shell.git
cd custom-shell

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the shell
python main.py
```

### API Key Setup

Get your free API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

You can either:
- Set environment variable: `export GEMINI_API_KEY=your_key_here` (Mac/Linux) or `set GEMINI_API_KEY=your_key_here` (Windows)
- Enter it when prompted at startup

## Usage

### Natural Language Commands

```
C:\custom-shell> list files in current directory
Intent: {'action': 'list', 'path': '.'}
Execute: dir .? (y/n/preview/dry-run): y
[Shows directory contents]

C:\custom-shell> go to parent directory
Intent: {'action': 'change_dir', 'path': '..'}
Execute: cd ..? (y/n/preview/dry-run): y
[Changes directory]
```

### Shell Commands

Prefix with `!` to execute traditional shell commands:

```
C:\custom-shell> !echo Hello World
Execute: echo Hello World? (y/n/preview/dry-run): y
Hello World
```

### Script Generation

```
C:\custom-shell> script backup my documents
Generated script:
#!/bin/bash
# Backup script...

Save as (filename.sh): backup.sh
Script saved to backup.sh
```

### Script Augmentation

```
C:\custom-shell> augment error_handling backup.sh
[Adds comprehensive error handling to your script]
```

### Available Commands

- `help` - Show help information
- `exit` or `quit` - Exit the shell
- `script <description>` - Generate a script from natural language
- `augment <action> <script>` - Modify scripts (actions: `refactor`, `error_handling`, `test_stubs`)

### Execution Options

When prompted to execute a command:
- `y` - Execute the command
- `n` - Skip execution
- `preview` or `dry-run` - Simulate execution without making changes

## 🏗️ Architecture

```
┌─────────────────┐
│  Frontend REPL  │  Interactive terminal interface
└────────┬────────┘
         │
    ┌────▼────┐
    │ Intent  │  Parse NL → JSON intent
    │ Parser  │  (Gemini API + fallbacks)
    └────┬────┘
         │
    ┌────▼────────┐
    │  Command    │  Intent → Shell command
    │  Generator  │  (Cross-platform)
    └────┬────────┘
         │
    ┌────▼────────┐
    │  Planner &  │  Safety checks, dry-run
    │  Safety     │  Affected files analysis
    └────┬────────┘
         │
    ┌────▼────────┐
    │  Executor   │  Subprocess execution
    │             │  (Timeout, sandboxing)
    └────┬────────┘
         │
    ┌────▼────────┐
    │  Context &  │  Session state, history
    │  Memory     │  Working directory tracking
    └─────────────┘
```

## 🔒 Safety Features

- **Destructive Command Detection** - Blocks dangerous operations like `rm -rf /`
- **Dry-Run Mode** - Preview commands before execution
- **Confirmation Prompts** - User approval required for all commands
- **Affected Files Analysis** - Shows what files will be modified
- **Timeout Protection** - Commands automatically terminate after 30 seconds
- **Audit Trail** - All actions logged to `audit.log`


## 🤝 Contributing

Contributions welcome! Areas for enhancement:
- Additional AI provider support (OpenAI, Claude, etc.)
- Enhanced sandboxing with containers/VMs
- Plugin system for bash/zsh integration
- More sophisticated intent parsing
- Interactive command editing

---

**Note**: This shell executes real system commands. Always review commands before confirming execution, especially when learning how it interprets natural language.