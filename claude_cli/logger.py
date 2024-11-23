import logging
import click


class ColoredLogger(logging.Logger):
    """Custom logger that uses Click colors for output"""

    COLORS = {
        logging.DEBUG: dict(fg="blue"),
        logging.INFO: dict(fg="green"),
        logging.WARNING: dict(fg="yellow"),
        logging.ERROR: dict(fg="red"),
        logging.CRITICAL: dict(fg="red", bold=True),
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


def setup_logging(debug: bool = False):
    """Configure the custom logger"""
    # Register our custom logger class
    logging.setLoggerClass(ColoredLogger)

    # Get logger instance
    logger = logging.getLogger("claude-cli")
    logger.setLevel(logging.DEBUG if debug else logging.INFO)

    return logger
