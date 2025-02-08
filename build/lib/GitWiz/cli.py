from .autocommit import gitmanager
from colorama import Fore, init
import pyfiglet
init(autoreset=True)
from .readmegenerator import Generate_class

COMMAND_HELP = {
    "configure": "Configure Git settings email and username to access github for this repository (necessary only 1 time).",
    "commit": "Commit changes with a commit message.",
    "push": "Push commits to the remote repository.",
    "pull": "Pull the latest changes from the remote repository.if any error comes its may be because github repo is empty continue with your next operations",
    "checkout": "Switch branches or restore working tree files.",
    "generate_readme": "Generate a README file for your project.you need mistral running on your computer using ollama",
    "help": "Show help for commands. Usage: 'help <command>' or 'help' for all commands.",
    "auto":"automatically does all the operations for you. If any error occured use other commands instead of auto(happens in conflict).",
    "exit": "Exit Git Wiz."
}

def display_banner():
    banner = pyfiglet.figlet_format("Git Wiz")
    print(Fore.CYAN + banner)
    print(Fore.YELLOW + "Welcome to Git Manager - Simplify your Git workflows!\n")
    print(Fore.GREEN + "Choose your actions and manage your repositories with ease you can automate readme file creation too.\n")
    print(Fore.GREEN + "Please configure first if you are using it first time.")

def show_help(command=None):
    if command:
        if command in COMMAND_HELP:
            print(Fore.CYAN + f"{command}: " + Fore.YELLOW + COMMAND_HELP[command])
        else:
            print(Fore.RED + f"Unknown command: {command}. Type 'help' for available commands.")
    else:
        print(Fore.GREEN + "Available commands:")
        for cmd, desc in COMMAND_HELP.items():
            print(Fore.CYAN + f"{cmd}: " + Fore.YELLOW + desc)

def main():
    display_banner()
    repo_path = input(Fore.BLUE + "Enter the Git repository path: ").strip()
    if not repo_path:
        print(Fore.RED + "Repository path is required!")
        return
    manager = gitmanager(repo_path)


    while True:
        print(Fore.YELLOW + "\nAvailable commands: configure, commit, push, pull, checkout, generate_readme, auto, exit")
        command = input(Fore.CYAN + "Enter command: ").strip().lower()
        if command == "exit":
            print(Fore.RED + "Exiting Git Ease...")
            break
        elif command == "help":
            show_help()
        elif command.startswith("help "):
            _, cmd = command.split(maxsplit=1)
            show_help(cmd)
        elif hasattr(manager, command):
            getattr(manager, command)()
        else:
            print(Fore.RED + "Invalid action. Please try again.")

if __name__ == "__main__":
    main()
