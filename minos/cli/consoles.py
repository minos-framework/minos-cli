from rich.console import (
    Console,
)

console = Console(width=120)
error_console = Console(width=120, stderr=True, style="bold red")
