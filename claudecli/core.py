import os
import logging
from typing import Optional
from dataclasses import dataclass
from anthropic import Anthropic


@dataclass
class ShellConfig:
    """Shell configuration and detection"""

    name: str
    path: str
    rc_file: str

    @classmethod
    def detect_current_shell(cls) -> "ShellConfig":
        """Detect the current shell environment"""
        shell_path = os.environ.get("SHELL", "")
        shell_name = os.path.basename(shell_path)

        shell_configs = {
            "bash": cls("bash", shell_path, ".bashrc"),
            "zsh": cls("zsh", shell_path, ".zshrc"),
            "fish": cls("fish", shell_path, ".config/fish/config.fish"),
            # Add more shells as needed
        }

        return shell_configs.get(shell_name, cls("sh", "/bin/sh", ""))  # Default to sh


class ClaudeCLI:
    def __init__(self, api_key: Optional[str] = None, shell: Optional[ShellConfig] = None):
        if api_key is None and "ANTHROPIC_API_KEY" not in os.environ:
            raise ValueError(
                "ANTHROPIC_API_KEY is required to use ClaudeCLI. Please obtain an API key from: https://console.anthropic.com/settings/keys"
            )
        self.client = Anthropic(api_key=api_key)
        self.shell = shell or ShellConfig.detect_current_shell()
        self.logger = logging.getLogger("claude-cli")

    def get_command(self, description: str) -> str:
        """Generate shell command using Claude"""
        prompt = f"""Given this request: "{description}"
        Target shell: {self.shell.name}
        
        Generate ONLY the exact shell command(s) to accomplish this. 
        Use shell-specific syntax and features when beneficial.
        No explanations or markdown formatting - just the raw command(s).
        If multiple commands are needed, join them with && or ;
        Ensure the command is safe and won't cause data loss."""

        message = self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=100,
            temperature=0,
            messages=[{"role": "user", "content": prompt}],
        )

        return message.content[0].text.strip()

    def should_proceed(self, command: str) -> str:
        """Check command safety using Claude Haiku"""
        prompt = f"""As a {self.shell.name} command safety checker, analyze this command and respond with EXACTLY one word:
        Command: {command}
        
        If the command appears safe and reasonable, respond with "PROCEED".
        If the command looks dangerous, unusual, or potentially destructive, respond with "CONFIRM".
        If the command could be catastrophic or requires human review, respond with "STOP".
        
        One word response:"""

        message = self.client.messages.create(
            model="claude-3-haiku-20240307", 
            max_tokens=10, 
            temperature=0, 
            messages=[{"role": "user", "content": prompt}]
        )

        return message.content[0].text.strip() if len(message.content) > 0 else message.content.text
