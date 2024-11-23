import sys
import subprocess
import traceback
import click
from typing import Optional
from claudecli.logger import setup_logging
from claudecli.core import ClaudeCLI, ShellConfig


@click.command()
@click.argument("command_description")
@click.option("--no-confirm", "-nc", is_flag=True, default=False, help="Execute without confirmation")
@click.option("--api-key", help="Anthropic API key (or set ANTHROPIC_API_KEY env var)")
@click.option("--shell", help="Specify shell to use (bash/zsh/fish)")
@click.option("--debug", is_flag=True, help="Show debug information")
def main(command_description: str, no_confirm: bool, api_key: str, shell: Optional[str], debug: bool):
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

        with click.progressbar(length=1, label="Generating command") as bar:
            shell_command = cli.get_command(command_description)
            bar.update(1)

        logger.debug("Generated command:\n")
        logger.info(shell_command)

        if not no_confirm:
            logger.debug("Checking safety level...")
            safety_level = cli.should_proceed(shell_command)
            if safety_level == "STOP":
                logger.critical("This command requires careful review!")
                logger.error("It might be destructive or have unintended consequences.")
                if not click.confirm("Are you absolutely sure you want to proceed?", default=False):
                    logger.warning("Aborted.")
                    return

            elif safety_level == "CONFIRM":
                logger.warning("This command should be reviewed")
                if not click.confirm("Would you like to proceed?", default=True):
                    logger.warning("Aborted.")
                    return

            else:  # PROCEED
                logger.debug("Command looks safe!")
                if debug:
                    logger.debug(f"Safety level: {safety_level}")

        logger.debug("Executing command...")

        # Use the detected/specified shell
        process = subprocess.run([shell_config.path, "-c", shell_command], text=True, capture_output=True)

        if process.stdout:
            click.echo(process.stdout)
        if process.stderr:
            click.echo(process.stderr, err=True)

        if process.returncode == 0:
            logger.debug("Command completed successfully!")
        else:
            logger.error(f"Command failed with error code: {process.returncode}")

        sys.exit(process.returncode)

    except Exception as e:
        logger.exception(f"Error:\n{str(e)}")
        logger.error(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
