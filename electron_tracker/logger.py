# Imports
from rich import print

# Constants
CRIT = 0
WARN = 1
INFO = 2
DEBUG = 3

# Set default
LOG_LEVEL = INFO

# Logging Functions
def debug(msg: str) -> str:
    if LOG_LEVEL >= DEBUG:
        print(f"[bold green][$] {msg}[/bold green]")

def info(msg: str) -> str:
    if LOG_LEVEL >= INFO:
        print(f"[bold cyan][+] {msg}[/bold cyan]")
    
def warn(msg: str) -> str:
    if LOG_LEVEL >= WARN:
        print(f"[bold orange_red1][!] {msg}[/bold orange_red1]")
    
def crit(msg: str) -> str:
    if LOG_LEVEL >= CRIT:
        print(f"[bold red][💀] {msg}[/bold red]")