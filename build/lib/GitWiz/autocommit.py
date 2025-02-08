import os
import git
from colorama import Fore, init
from .readmegenerator  import Generate_class

init(autoreset=True)

class gitmanager:
    def __init__(self,repo_path):
        self.user_name=""
        self.user_email=""
        self.repo_path=repo_path
        self.initialize_repo()
        self.add_remote()
        self.repo=git.Repo(self.repo_path)
        self.commit_message=""
        self.branch_name=""

    def configure(self):
        try:
            self.user_name = input("Enter Git username: ").strip()
            self.user_email = input("Enter Git email: ").strip()
            git.Git().config("--global", "user.name", self.user_name)
            git.Git().config("--global", "user.email", self.user_email)
            print(Fore.GREEN + f"Git username set to '{self.user_name}' with email '{self.user_email}'")
        except Exception as e:
            print(Fore.RED + f"Failed to set Git configuration: {e}")
            print(Fore.RED + "try again")

    def initialize_repo(self):
        if not os.path.exists(os.path.join(self.repo_path, ".git")):
            try:
                git.Repo.init(self.repo_path)
                print(Fore.GREEN + f"Initialized an empty Git repository in {self.repo_path}")
            except Exception as e:
                print(Fore.RED + f"Failed to initialize Git repository: {e}")
                print(Fore.RED + "try again")
                return False
        else:
            print(Fore.CYAN + "Git repository already initialized.")
        return True

    def add_remote(self):
        try:
            remote_name = "origin"   #input("Enter remote name (e.g., 'origin'): ").strip()
            remote_url = input("Enter GitHub repository URL: ").strip()
            if remote_name and remote_url:
                repo = git.Repo(self.repo_path)
                if repo.remotes:
                    repo.delete_remote(remote_name)
                repo.create_remote(remote_name, remote_url)
                print(Fore.GREEN + f"Remote '{remote_name}' added with URL: {remote_url}")
            else:
                print(Fore.RED + "Remote name and URL cannot be empty.")
        except git.exc.GitCommandError as e:
            print(Fore.RED + f"Failed to add remote: {e}")

    def commit(self):
        try:
            self.commit_message=input("enter commit message")
            if self.repo.is_dirty(untracked_files=True):
                self.repo.git.add(all=True)
                self.repo.index.commit(self.commit_message)
                print(Fore.GREEN + f"Committed changes with message: '{self.commit_message}'")
            else:
                print(Fore.CYAN + "No changes detected to commit.")
        except git.exc.InvalidGitRepositoryError:
            print(Fore.RED + f"The directory '{self.repo_path}' is not a valid Git repository.")
        except Exception as e:
            print(Fore.RED + f"An error occurred during commit: {e}")

    def checkout(self):
        try:
            branch_name = input("Enter branch name: ").strip()

            if branch_name not in [branch.name for branch in self.repo.branches]:  # or self.repo.heads
                print(Fore.CYAN + f"Branch '{branch_name}' does not exist locally.")

                remote_branches = self.repo.git.branch('-r').split('\n')
                remote_branch_name =  f"origin/{branch_name}"
                if any(remote_branch_name in branches.strip() for branches in remote_branches):
                    print(Fore.CYAN + f"Branch '{branch_name}' found on remote. Checking out...")
                    self.repo.git.checkout('-b', branch_name, remote_branch_name)

                else:
                    print(Fore.YELLOW + f"Branch '{branch_name}' not found on remote. Creating it locally...")
                    self.repo.git.checkout('-b', branch_name)

            else:
                print(Fore.CYAN + f"Switching to branch '{branch_name}'...")
                self.repo.git.checkout(branch_name)

            print(Fore.GREEN + f"Checked out branch '{branch_name}'.")
            return branch_name
        except Exception as e:
            print(Fore.RED + f"Failed to checkout branch: {e}")
            return None

    def pull(self):
        try:
            print(Fore.CYAN + "Available branches locally:")
            for branch in self.repo.branches:
                print(Fore.GREEN + branch.name)
            branch_name = self.checkout()

            if branch_name:
                print(Fore.CYAN + f"Pulling changes from origin/{branch_name} with rebase...")
                self.repo.git.pull("origin", branch_name, "--rebase")
                print(Fore.GREEN + f"Branch '{branch_name}' is up-to-date.")
            else:
                print(Fore.RED + "Pull operation canceled due to failed branch checkout.")

        except git.exc.GitCommandError as e:
            print(Fore.RED + f"Git command failed: {e}")
        except Exception as e:
            print(Fore.RED + f"An error occurred: {e}")

    def push(self):
        if not self.branch_name:
            self.branch_name = self.repo.active_branch.name
            print(Fore.YELLOW + f"branch name set to {self.branch_name}")
        try:
            if self.repo.is_dirty(untracked_files=True):
                print(Fore.YELLOW + "Warning: You have uncommitted changes. Consider Commiting them before pushing.")
                proceed = input("Do you want to continue without committing? (y/n): ").strip().lower()
                if proceed == 'n':
                    print(Fore.RED + "Push canceled.")
                    return

            if "origin" not in [remote.name for remote in self.repo.remotes]:
                print(Fore.RED + "Remote 'origin' not found. Please add a remote first.")
                return

            if self.branch_name not in [ref.name.split('/')[-1] for ref in self.repo.refs if ref.tracking_branch()]:
                print(Fore.CYAN + f"Setting upstream for '{self.branch_name}'...")
                self.repo.git.push("--set-upstream", "origin", self.branch_name)
            else:
                print(Fore.GREEN + f"Pushing changes to origin/{self.branch_name}...")
                self.repo.git.push("origin", self.branch_name)

            print(Fore.GREEN + f"Changes pushed to branch '{self.branch_name}'.")
        except git.exc.GitCommandError as e:
            print(Fore.RED + f"Git command failed: {e}")
        except Exception as e:
            print(Fore.RED + f"Failed to push changes: {e}")

    def generate_readme(self):
        generator=Generate_class(self.repo_path)
        generator.generate()

    def auto(self):
        #self.add_remote()
        self.pull()
        ip=input('do you want readme file y for yes and n for no')
        if ip=='y':
            self.generate_readme()
        self.commit()

        self.push()




