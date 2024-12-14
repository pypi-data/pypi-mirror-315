import os, sys, subprocess, readline # NOQA
# above line is noqa due to readline not being used.
import webbrowser

from pathlib import Path

from colorama import Style, Fore, Back

def error(text: str) -> None:
    print(f"🚨 {Fore.RED}error: {text}{Style.RESET_ALL}")
def hint(text: str) -> None:
    print(f"ℹ️  {Fore.BLUE}hint: {text}{Style.RESET_ALL}")
    # two spaces are on purpose!!
def warning(text: str) -> None:
    print(f"⚠️  {Fore.YELLOW}warning: {text}{Style.RESET_ALL}")
    # two spaces are on purpose!!
def important(text: str) -> None:
    print(f"⚠️  {Back.YELLOW}{Fore.BLACK}important: {text}{Style.RESET_ALL}")
    # two spaces are on purpose!!
def info(text: str) -> None:
    print(f"➤➤ {text}")

class MutablePath:
    def __init__(self, path: Path | None = None):
        self.root: str = os.path.abspath(os.sep)
        self.path: Path = path or Path(self.root)
        self.set(str(self.path), [])
    def set(self, path: str, cd_history: list[str]):
        old_path = self.path
        if path == "..":
            self.path = self.path.parent
        elif path == ".":
            ...
        else:
            self.path /= path
        if not os.path.exists(str(self.path)):
            error(f"{self.path} is not a valid path.")
            self.path = old_path
        else:
            cd_history.append(str(old_path))

def subprocess_run(command: list[str]):
    try:
        subprocess.run(command)
    except Exception as exc:
        error(f"solo: {exc}")

def main() -> None:
    at: str = os.getcwd()
    if len(sys.argv) > 1:
        at = sys.argv[1]
    mutable_location: MutablePath = MutablePath(Path(at))
    solo_mode: bool = False
    cd_history: list[str] = []
    while True:
        try:
            loc: Path = mutable_location.path
            if solo_mode:
                command: str = "solo " + input(
                    f"{Fore.YELLOW}<{os.name}>{Style.RESET_ALL} {str(loc)} {Fore.MAGENTA}"
                    f"[solo]{Style.RESET_ALL}{Fore.BLUE}>{Style.RESET_ALL} ")
                if command == "solo exit":
                    solo_mode = False
                    info("Exited solo")
                    continue
            else:
                command: str = input(f"{Fore.YELLOW}<{os.name}>{Style.RESET_ALL} {str(loc)}{Fore.BLUE}>{Style.RESET_ALL} ")

            # Split command into parts
            parts: list[str] = command.split(" ")
            new: list[str] = []
            string: str = ""

            for part in parts:
                if not part:
                    # Skip empty parts
                    continue
                elif string:
                    # If currently inside a quoted string
                    if part[-1] == string:
                        # Closing quote found
                        new[-1] += " " + part[:-1]
                        string = ""
                    else:
                        # Append part to the current quoted string
                        new[-1] += " " + part
                elif part[0] in "\"'":
                    # Opening quote found
                    if len(part) > 1 and part[-1] == part[0]:
                        # Handle single-word quoted strings
                        new.append(part[1:-1])
                    else:
                        # Start a new quoted string
                        new.append(part[1:])
                        string = part[0]
                else:
                    # Regular unquoted part
                    new.append(part)
            if string:
                error("unclosed string in command.")
                continue

            if not new:
                continue

            command: str = new[0]
            args: list[str] = new[1:]

            def run_solo():
                if args:
                    if args[0] in ["cd", "exit", "help"]:
                        warning(f"{args[0]} may not work properly when executing using solo")
                    subprocess_run(args)
                else:
                    nonlocal solo_mode
                    solo_mode = True
            def undo_cd():
                try:
                    mutable_location.set(cd_history.pop(), [])
                except IndexError:
                    warning("nothing left to undo")

            try:
                {
                    "exit": lambda: (info("Exited pistol"), exit()),
                    "cd": lambda: mutable_location.set(args[0], cd_history),
                    "ucd": lambda: undo_cd(),
                    "solo": run_solo,
                    "help": lambda: webbrowser.open("https://github.com/pixilll/pistol")
                }[command]()
            except KeyError:
                error(f"{command} is not a valid command. try solo {command}")
        except KeyboardInterrupt:
            print()