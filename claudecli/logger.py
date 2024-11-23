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
            icon = self.ICONS.get(level, "")
            color_kwargs = self.COLORS.get(level, {})
            click.secho(f"{icon} {msg}", **color_kwargs)


def setup_logging(debug: bool = False):
    """Configure the custom logger"""
    logging.setLoggerClass(ColoredLogger)
    logger = logging.getLogger("claude-cli")
    logger.setLevel(logging.DEBUG if debug else logging.INFO)

    return logger
