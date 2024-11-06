#!/usr/bin/env python3
import os
import sys
import subprocess
import logging
import click
from typing import Optional
from dataclasses import dataclass
from anthropic import Anthropic

class ColoredLogger(logging.Logger):
    """Custom logger that uses Click colors for output"""
    
    COLORS = {
        logging.DEBUG: dict(fg='blue'),
        logging.INFO: dict(fg='green'),
        logging.WARNING: dict(fg='yellow'),
        logging.ERROR: dict(fg='red'),
        logging.CRITICAL: dict(fg='red', bold=True),
    }
    
    ICONS = {
        logging.DEBUG: "🔍",
        logging.INFO: "ℹ️ ",
        logging.WARNING: "⚠️ ",
        logging.ERROR: "❌",
        logging.CRITICAL: "☠️ ",
    }
    
    def __init__(self, name: str):
        super().__init__(name)
        self._previous_level = self.level
    
    def _log(self, level: int, msg: str, *args, **kwargs):
        if self.isEnabledFor(level):
            # Format message with args if any
            if args:
                msg = msg % args
            
            # Add icon and apply color
            icon = self.ICONS.get(level, "")
            color_kwargs = self.COLORS.get(level, {})
            colored_msg = click.style(f"{icon} {msg}", **color_kwargs)
            
            # Print to console
            click.echo(colored_msg)

@dataclass
class ShellConfig:
    """Shell configuration and detection"""
    name: str
    path: str
    rc_file: str
    
    @classmethod
    def detect_current_shell(cls) -> 'ShellConfig':
        """Detect the current shell environment"""
        shell_path = os.environ.get('SHELL', '')
        shell_name = os.path.basename(shell_path)
        
        shell_configs = {
            'bash': cls('bash', shell_path, '.bashrc'),
            'zsh': cls('zsh', shell_path, '.zshrc'),
            'fish': cls('fish', shell_path, '.config/fish/config.fish'),
            # Add more shells as needed
        }
        
        return shell_configs.get(shell_name, 
                               cls('sh', '/bin/sh', ''))  # Default to sh

class ClaudeCLI:
    def __init__(self, api_key: Optional[str] = None, shell: Optional[ShellConfig] = None):
        self.client = Anthropic(api_key=api_key)
        self.shell = shell or ShellConfig.detect_current_shell()
        self.logger = logging.getLogger('claude-cli')
        
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
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        return message.content.strip()
    
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
            max_tokens=1,
            temperature=0,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        return message.content.strip()

def setup_logging(debug: bool = False):
    """Configure the custom logger"""
    # Register our custom logger class
    logging.setLoggerClass(ColoredLogger)
    
    # Get logger instance
    logger = logging.getLogger('claude-cli')
    logger.setLevel(logging.DEBUG if debug else logging.INFO)
    
    return logger

@click.command()
@click.argument('command_description')
@click.option('--no-confirm', is_flag=True, help='Execute without confirmation')
@click.option('--api-key', help='Anthropic API key (or set ANTHROPIC_API_KEY env var)')
@click.option('--shell', help='Specify shell to use (bash/zsh/fish)')
@click.option('--debug', is_flag=True, help='Show debug information')
def main(command_description: str, no_confirm: bool, api_key: str, 
         shell: Optional[str], debug: bool):
    """Natural language interface for command line using Claude"""
    
    logger = setup_logging(debug)
    
    try:
        # Configure shell
        if shell:
            shell_config = ShellConfig(shell, f"/bin/{shell}", f".{shell}rc")
            logger.debug(f"Using specified shell: {shell}")
        else:
            shell_config = ShellConfig.detect_current_shell()
            logger.debug(f"Detected shell: {shell_config.name} ({shell_config.path})")
        
        cli = ClaudeCLI(api_key=api_key, shell=shell_config)
        
        with click.progressbar(length=1, label='Generating command') as bar:
            shell_command = cli.get_command(command_description)
            bar.update(1)
        
        logger.info(f"Generated command:\n  {shell_command}")
        
        if not no_confirm:
            with click.progressbar(length=1, label='Analyzing safety') as bar:
                safety_level = cli.should_proceed(shell_command)
                bar.update(1)
            
            if safety_level == "STOP":
                logger.critical("This command requires careful review!")
                logger.error("It might be destructive or have unintended consequences.")
                if not click.confirm('Are you absolutely sure you want to proceed?', 
                                   default=False):
                    logger.warning("Aborted.")
                    return
            
            elif safety_level == "CONFIRM":
                logger.warning("This command should be reviewed")
                if not click.confirm('Would you like to proceed?', default=True):
                    logger.warning("Aborted.")
                    return
            
            else:  # PROCEED
                logger.info("Command looks safe!")
                if debug:
                    logger.debug(f"Safety level: {safety_level}")
        
        logger.info("Executing command...")
        
        # Use the detected/specified shell
        process = subprocess.run([shell_config.path, '-c', shell_command], 
                               text=True, capture_output=True)
        
        if process.stdout:
            click.echo(process.stdout)
        if process.stderr:
            click.echo(process.stderr, err=True)
            
        if process.returncode == 0:
            logger.info("Command completed successfully!")
        else:
            logger.error(f"Command failed with error code: {process.returncode}")
        
        sys.exit(process.returncode)
            
    except Exception as e:
        logger.critical(f"Error: {str(e)}")
        if debug:
            logger.debug("Debug traceback:", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()