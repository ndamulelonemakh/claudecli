# Claude CLI

Natural language interface for command line using Claude AI

## Installation

```bash
pip install claude-cli
```

## Usage

```bash
# Basic usage
claude "find all python files modified today"

# Skip confirmation
claude --no-confirm "list directory contents"

# Specify shell
claude --shell zsh "find large files"

# Debug mode
claude --debug "compress logs"
```

## Features

- Natural language command generation using Claude AI
- Automatic shell detection (bash/zsh/fish)
- Smart safety checks
- Colorful logging
- Progress indicators
- Debug mode

## Configuration

The CLI looks for the following environment variables:

- `ANTHROPIC_API_KEY`: Your Anthropic API key
- `CLAUDE_CLI_DEBUG`: Enable debug mode
- `CLAUDE_CLI_SHELL`: Override shell detection

## Development

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/claude-cli.git
   cd claude-cli
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   ```

3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

4. Run tests:
   ```bash
   tox
   ```
5. Publish a new release

   ```bash
   # Update version in __version__.py
   
   # Commit and changes
   git add .
   git commit -m "feat: new feature description"
   git tag -a v0.1.0 -m "Release v0.1.0"
   git push origin main --tags
   ````

## Project structure

```bash
claude-cli/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── publish-github.yml
│       └── publish-pypi.yml
├── src/
│   └── claude_cli/
│       ├── __init__.py
│       ├── __version__.py
│       ├── cli.py
│       ├── logger.py
│       ├── shell.py
│       └── core.py
├── tests/
│   ├── __init__.py
│   ├── test_cli.py
│   ├── test_logger.py
│   └── test_shell.py
├── .gitignore
├── LICENSE
├── MANIFEST.in
├── pyproject.toml
├── README.md
└── tox.ini
```

## Contributing

Pull requests are welcome!

## License

This project is licensed under the MIT License - see the LICENSE file for details.
