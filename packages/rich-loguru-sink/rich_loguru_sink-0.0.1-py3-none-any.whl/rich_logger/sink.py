"""The Rich Sink for the loguru logger."""

from pathlib import Path
from typing import Dict, List

from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)
from rich.style import Style
from rich.text import Text
from rich.traceback import install as tr_install
from rich_gradient import Color, Gradient

console = Console()
tr_install(console=console)


FORMAT: str = (
    "{time:HH:mm:ss.SSS} | Run {extra[run]} | {file.name: ^12} | Line {line} | {level} | {message}"
)
CWD: Path = Path.cwd()
LOGS_DIR: Path = CWD / "logs"
RUN_FILE: Path = LOGS_DIR / "run.txt"


def find_cwd():
    pass


def setup() -> int:
    """Setup the logger and return the run count."""
    if not LOGS_DIR.exists():
        LOGS_DIR.mkdir(parents=True)
        console.print(f"Created Logs Directory: {LOGS_DIR}")
    if not RUN_FILE.exists():
        with open(RUN_FILE, "w") as f:
            f.write("0")
            console.print("Created Run File, Set to 0")

    with open(RUN_FILE, "r", encoding="utf-8") as f:
        run = int(f.read())
        return run


def read() -> int:
    """Read the run count from the file."""
    with open(RUN_FILE, "r", encoding="utf-8") as f:
        run = int(f.read())
    return run


def write(run: int) -> None:
    """Write the run count to the file."""
    with open(RUN_FILE, "w", encoding="utf-8") as f:
        f.write(str(run))


def increment() -> int:
    """Increment the run count and write it to the file."""
    run = read()
    run += 1
    write(run)
    return run


LEVEL_STYLES: Dict[str, Style] = {
    "TRACE": Style(italic=True),
    "DEBUG": Style(color="#aaaaaa"),
    "INFO": Style(color="#00afff"),
    "SUCCESS": Style(bold=True, color="#00ff00"),
    "WARNING": Style(italic=True, color="#ffaf00"),
    "ERROR": Style(bold=True, color="#ff5000"),
    "CRITICAL": Style(bold=True, color="#ff0000"),
}

GRADIENTS: Dict[str, List[Color]] = {
    "TRACE": [Color("#888888"), Color("#aaaaaa"), Color("#cccccc")],
    "DEBUG": [Color("#338888"), Color("#55aaaa"), Color("#77cccc")],
    "INFO": [Color("#008fff"), Color("#00afff"), Color("#00cfff")],
    "SUCCESS": [Color("#00aa00"), Color("#00ff00"), Color("#afff00")],
    "WARNING": [Color("#ffaa00"), Color("#ffcc00"), Color("#ffff00")],
    "ERROR": [Color("#ff0000"), Color("#ff5500"), Color("#ff7700")],
    "CRITICAL": [Color("#ff0000"), Color("#ff005f"), Color("#ff00af")],
}
progress = Progress(
    TextColumn("[progress.description]{task.description}"),
    SpinnerColumn(),
    BarColumn(bar_width=None),
    MofNCompleteColumn(),
    TaskProgressColumn(),
    TimeElapsedColumn(),
    TimeRemainingColumn(),
    console=console,
)


def rich_sink(message) -> None:
    record = message.record
    level = record["level"].name
    colors = GRADIENTS[level]
    style = LEVEL_STYLES[level]

    # title
    title: Text = Gradient(
        f" {level} | {record['file'].name} | Line {record['line']} ", colors=colors
    ).as_text()
    title.highlight_words("|", style="italic #666666")
    title.stylize(Style(reverse=True))

    # subtitle
    run: int = read()
    subtitle: Text = Text.assemble(
        Text(f"Run {run}"),
        Text(" | "),
        Text(record["time"].strftime("%H:%M:%S.%f")[:-3]),
        Text(record["time"].strftime(" %p")),
    )
    subtitle.highlight_words(":", style="dim #aaaaaa")

    # Message
    message_text: Text = Gradient(record["message"], colors, style="bold")
    # Generate and print log panel with aligned title and subtitle
    log_panel: Panel = Panel(
        message_text,
        title=title,
        title_align="left",  # Left align the title
        subtitle=subtitle,
        subtitle_align="right",  # Right align the subtitle
        border_style=style + Style(bold=True),
        padding=(1, 2),
    )
    console.print(log_panel)
