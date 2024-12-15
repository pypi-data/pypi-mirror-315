import os, sys, subprocess, readline, webbrowser # NOQA
# above line is noqa due to readline not being used.

from pathlib import Path
from colorama import Style, Fore, Back

storage_path: Path = Path(__file__).parent / "storage"

def error(text: str) -> None:
    print(f"🚨 {Fore.RED}error: {text}{Style.RESET_ALL}")
def hint(text: str) -> None:
    print(f"💡 {Fore.BLUE}hint: {text}{Style.RESET_ALL}")
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
    def set(self, path: str, cd_history: list[str], ucd: bool = False, st: bool = False):
        old_path = self.path
        if str(self.path) == str(storage_path) and not ucd:
            warning("cannot cd out of storage mode, use st or ucd instead.")
            return
        if path == str(storage_path) and not st:
            hint("use the st command to switch to storage mode easier")
        if path == "..":
            self.path = self.path.parent
        elif path == ".":
            ...
        else:
            self.path /= path
        if not os.path.exists(str(self.path)) and st:
            warning("storage directory does not exist, creating now.")
            os.mkdir(str(self.path))
            info("storage directory created successfully")
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
            disp_loc: str = f"{Back.YELLOW}{Fore.BLACK}storage{Style.RESET_ALL}" if str(loc) == str(storage_path) else loc
            try:
                if solo_mode:
                    command: str = "solo " + input(
                        f"➤➤ {Fore.YELLOW}<{os.name}>{Style.RESET_ALL} {disp_loc} {Fore.MAGENTA}"
                        f"[solo]{Style.RESET_ALL}{Fore.BLUE}>{Style.RESET_ALL} ")
                    if command == "solo exit":
                        solo_mode = False
                        info("exited solo")
                        continue
                else:
                    command: str = input(f"➤➤ {Fore.YELLOW}<{os.name}>{Style.RESET_ALL} {disp_loc}{Fore.BLUE}>{Style.RESET_ALL} ")
            except EOFError:
                print()
                try:
                    import getpass

                    hint("press ^C to exit pistol")
                    hint("press any other button to return to pistol")

                    getpass.getpass(f"➤➤ ")
                    continue
                except KeyboardInterrupt:
                    command: str = "exit --no-hint"
                    print()
                except EOFError:
                    print()
                    continue

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

            try:
                def run_solo():
                    if args:
                        force_cwd: bool = False
                        if "--force-cwd" in args:
                            args.remove("--force-cwd")
                            force_cwd = True
                        if args[0] in ["cd", "exit", "help", "version", "clear", "cls", "st", "ucd"]:
                            warning(f"{args[0]} may not work properly when executing using solo")
                        old_dir: str = os.getcwd()
                        try:
                            os.chdir(loc)
                        except FileNotFoundError:
                            if force_cwd:
                                info(f"created {disp_loc}")
                                os.mkdir(loc)
                                os.chdir(loc)
                            else:
                                warning(f"tried to execute a solo command in a directory that does not exist. solo will execute it in {old_dir} instead.")
                                hint(f"rerun the command with the --force-cwd option to run in {disp_loc}.")
                        subprocess_run(args)
                        os.chdir(old_dir)
                    else:
                        nonlocal solo_mode
                        solo_mode = True
                def undo_cd():
                    try:
                        mutable_location.set(cd_history.pop(), [], ucd=True)
                    except IndexError:
                        warning("nothing left to undo")

                from . import VERSION

                try:
                    {
                        "exit": lambda: (
                            info("exited pistol"),
                            hint("pressing ^D chord to ^C will exit pistol as well") if "--no-hint" not in args else ...,
                            exit()
                        ),
                        "cd": lambda: mutable_location.set(args[0], cd_history),
                        "ucd": undo_cd,
                        "solo": run_solo,
                        "clear": lambda: subprocess.run("clear"),
                        "cls": lambda: subprocess.run("clear"),
                        "help": lambda: webbrowser.open("https://github.com/pixilll/pistol"),
                        "version": lambda: info(f"pistol {VERSION}"),
                        "st": lambda: (
                            mutable_location.set(str(storage_path), cd_history, st=True),
                            hint("use st again to return to normal mode")) if str(loc) != str(storage_path) else undo_cd()
                    }[command]()
                except KeyError:
                    error(f"{command} is not a valid command")
                    hint(f"try solo {command}")
            except IndexError:
                error(f"not enough arguments supplied for {command}")
        except KeyboardInterrupt:
            print()