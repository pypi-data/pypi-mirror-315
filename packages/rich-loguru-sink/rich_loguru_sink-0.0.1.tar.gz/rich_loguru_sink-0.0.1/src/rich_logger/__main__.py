"""Rich logger setup and usage."""

import sys
import atexit

from loguru import logger

from rich_logger.sink import FORMAT, LOGS_DIR, increment, read, rich_sink, setup


def get_logger():
    """Initialize the logger with two sinks and return it."""
    run = setup()
    logger.remove()
    logger.configure(
        handlers=[
            {
                "sink": rich_sink,
                "format": "{message}",
                "level": "INFO",
                "backtrace": True,
                "diagnose": True,
                "colorize": False,
            },
            {
                "sink": str(LOGS_DIR / "trace.log"),
                "format": FORMAT,
                "level": "TRACE",
                "backtrace": True,
                "diagnose": True,
                "colorize": False,
            },
        ],
        extra={"run": run},
    )
    return logger


def on_exit():
    run = read()
    logger.info(f"Run {run} Completed")
    run = increment()


atexit.register(on_exit)

if __name__ == "__main__":
    logger = get_logger()

    logger.info("Started")
    logger.trace("Trace")
    logger.debug("Debug")
    logger.info("Info")
    logger.success("Success")
    logger.warning("Warning")
    logger.error("Error")
    logger.critical("Critical")

    logger.info("Finished")
    sys.exit(0)
