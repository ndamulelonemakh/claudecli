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

## Configuration

The CLI looks for the following environment variables:

- `ANTHROPIC_API_KEY`: Your Anthropic API key
- `CLAUDE_CLI_DEBUG`: Enable debug mode
- `CLAUDE_CLI_SHELL`: Override shell detection

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

Pull requests are definitely welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
