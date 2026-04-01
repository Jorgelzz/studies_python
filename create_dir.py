import os
import shutil
import subprocess
import sys
import datetime
from time import sleep

from rich.console import Console
from rich.progress import track
from rich.prompt import Prompt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
today = datetime.date.today()


def create_dir(path):
    if not os.path.exists(path):
        for _ in track(
            range(100),
            description="[green]Creating directory[/green]",
            transient=True,
        ):
            sleep(0.02)
        os.makedirs(path)
        print(f"Directory created: {path}")
    else:
        print(f"Directory already exists: {path}")
        return False


def _cursor_launch_argv(folder: str) -> list[str] | None:
    """Resolve how to open a folder in Cursor (PATH or default Windows install)."""
    if sys.platform == "win32":
        exe = os.path.join(
            os.environ.get("LOCALAPPDATA", ""),
            "Programs",
            "cursor",
            "Cursor.exe",
        )
        if os.path.isfile(exe):
            return [exe, folder]
    found = shutil.which("cursor")
    if found:
        return [found, folder]
    return None


def show_options_menu(target_dir: str) -> None:
    console = Console()
    console.print()
    console.print("[bold bright_cyan]1[/bold bright_cyan] - Open folder in File Explorer")
    console.print("[bold bright_magenta]2[/bold bright_magenta] - Open folder in Cursor")
    console.print("[bold bright_yellow]3[/bold bright_yellow] - Exit")
    choice = Prompt.ask(
        "[bold white]Choose[/bold white]",
        choices=["1", "2", "3"],
        default="3",
    )
    target_dir = os.path.normpath(os.path.abspath(target_dir))

    if choice == "1":
        if sys.platform == "win32":
            os.startfile(target_dir)
        else:
            subprocess.run(["xdg-open", target_dir], check=False)
    elif choice == "2":
        argv = _cursor_launch_argv(target_dir)
        if argv is None:
            console.print(
                "[red]Cursor not found. Install it or add the 'cursor' command to PATH.[/red]"
            )
        else:
            result = subprocess.run(argv, shell=False, capture_output=True)
            if result.returncode != 0:
                console.print(
                    "[red]Cursor exited with an error. Try opening the folder manually.[/red]"
                )


if __name__ == "__main__":
    path = os.path.join(BASE_DIR, today.strftime("%Y-%m-%d"))
    create_dir(path)
    show_options_menu(path)
