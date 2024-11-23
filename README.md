# Claude CLI

Natural language interface for command line using Claude AI

## Installation

```bash
pip install claudecli
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

- `ANTHROPIC_API_KEY`: Your Anthropic API key (**Required**)
- `CLAUDE_CLI_DEBUG`: Enable debug mode
- `CLAUDE_CLI_SHELL`: Override shell detection

## Project structure

```bash
.
├── LICENSE
├── README.md
├── claude_cli
│   ├── __init__.py
│   ├── cli.py
│   ├── core.py
│   └── logger.py
└── pyproject.toml
```

## Contributing

Pull requests are definitely welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
