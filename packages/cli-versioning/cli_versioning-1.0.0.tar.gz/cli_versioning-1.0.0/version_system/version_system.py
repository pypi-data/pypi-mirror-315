from colorama import Fore, Style
from datetime import datetime
import argparse
import json
import os

class TypeVersionSystem:
    def __init__(self, major:str='Major', minor:str='Minor',patch:str='Patch') -> None:
        self.major:str = major.title()
        self.minor:str = minor.title()
        self.patch:str = patch.title()
    
    def __dict__(self) -> dict:
        return {
            "major": self.major,
            "minor": self.minor,
            "patch": self.patch
        }

class Project:
    def __init__(self, name:str='', description:str='', author:str='', email:str='', license:str='', year:str='') -> None:
        self.name:str = name
        self.description:str = description
        self.author:str = author
        self.email:str = email
        self.license:str = license
        self.year:str = year

    def __str__(self) -> str:
        header = (
            f"{Fore.BLUE}{Style.BRIGHT}"
            f"{'=' * 40}\n"
            f"{' PROJECT INFO ':^40}\n"
            f"{'=' * 40}{Style.RESET_ALL}\n"
        )
        details = (
            f"{Style.BRIGHT}{Fore.CYAN}Project:{Style.RESET_ALL} {self.name}\n"
            f"{Fore.GREEN}Description:{Style.RESET_ALL} {self.description}\n"
            f"{Fore.YELLOW}Author:{Style.RESET_ALL} {self.author}\n"
            f"{Fore.MAGENTA}Email:{Style.RESET_ALL} {self.email}\n"
            f"{Fore.RED}License:{Style.RESET_ALL} {self.license}\n"
            f"{Fore.LIGHTBLACK_EX}Year:{Style.RESET_ALL} {self.year}\n"
        )
        footer = f"{Fore.BLUE}{Style.BRIGHT}{'=' * 40}{Style.RESET_ALL}\n"
        return header + details + footer

    def __repr__(self) -> str:
        return f"{self.name} - {self.description} - {self.author} - {self.email} - {self.url} - {self.license} - {self.year}"

    def __dict__(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "author": self.author,
            "email": self.email,
            "license": self.license,
            "year": self.year
        }

class VersionSystem:
    def __init__(self, typeVersionSystem:TypeVersionSystem=TypeVersionSystem(), project:Project=Project()) -> None:
        """
        Initializes version and change history.
        Starts with version 1.0.0.
        """
        self.___major:int = 1
        self.___minor:int = 0
        self.___patch:int = 0
        self.___history:list = []
        self.___typeVersionSystem:TypeVersionSystem = typeVersionSystem
        self.___project:Project = project
        self.___filename:str = "version.json"
        self.___load_from_json()
        self.___save_to_json()   

    def ___set_type_version_system(self, major:str, minor:str, patch:str) -> None:
        """
        Sets the type of version system.

        :param typeVersionSystem: Type of version system.
        """
        if not major or not minor or not patch:
            return
        self.___typeVersionSystem = TypeVersionSystem(major, minor, patch)

    def __repr__(self) -> str:
        f"""
        Returns the current version in the format  0.0.0.
        """
        return f"{self.___major}.{self.___minor}.{self.___patch}"
    
    def __str__(self) -> str:
        """
        Returns the current version with styled colors for printing.

        :return: Styled string with version in the format 0.0.0.
        """
        return (
            f"{Style.BRIGHT}{Fore.YELLOW}Version: {Style.RESET_ALL}"
            f"{Style.BRIGHT}{Fore.RED}{self.___major}{Style.RESET_ALL}."
            f"{Fore.GREEN}{self.___minor}{Style.RESET_ALL}."
            f"{Fore.BLUE}{self.___patch}{Style.RESET_ALL}"
        )

    def __dict__(self) -> dict:
        """
        Returns the current version in dictionary format.

        :return: Dictionary with the current version.
        """
        return {
            self.___typeVersionSystem.major: self.___major,
            self.___typeVersionSystem.minor: self.___minor,
            self.___typeVersionSystem.patch: self.___patch
        }
    
    def ___info(self) -> str:
        """
        Returns the current version with project information.

        :return: String with version and project information.
        """
        return (
            f"{Fore.GREEN} {Style.BRIGHT} {'='*50}\n"
            f"{'VERSION':^50}\n"
            f"{'='*50}{Style.RESET_ALL}\n\n"
            f"{Style.BRIGHT}{Fore.GREEN}Version: {Fore.RED}{self.___major}{Style.RESET_ALL}."
            f"{Fore.GREEN}{self.___minor}{Style.RESET_ALL}."
            f"{Fore.BLUE}{self.___patch}{Style.RESET_ALL}\n"
            f"{Style.BRIGHT}{Fore.GREEN}Project: {Fore.CYAN}{self.___project.name}{Style.RESET_ALL}\n"
            f"{Style.BRIGHT}{Fore.GREEN}Description: {Fore.LIGHTMAGENTA_EX}{self.___project.description}{Style.RESET_ALL}\n"
            f"{Style.BRIGHT}{Fore.GREEN}Author: {Fore.YELLOW}{self.___project.author}{Style.RESET_ALL}\n"
            f"{Style.BRIGHT}{Fore.GREEN}Email: {Fore.MAGENTA}{self.___project.email}{Style.RESET_ALL}\n"
            f"{Style.BRIGHT}{Fore.GREEN}License: {Fore.LIGHTRED_EX}{self.___project.license}{Style.RESET_ALL}\n"
            f"{Style.BRIGHT}{Fore.GREEN}Year: {Fore.LIGHTWHITE_EX}{self.___project.year}{Style.RESET_ALL}\n\n"
            f"{Fore.GREEN + Style.BRIGHT}{'='*50} {Style.RESET_ALL}"
        )

    def ___load_from_json(self) -> None:
        """
        Loads the state of the version system and project from a JSON file.
        """
        if not os.path.exists(self.___filename):
            return
        
        with open(self.___filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        project_data = data.get("project", {})
        self.___project = Project(**project_data)
        type_data = data.get("__type", {})
      
        self.___set_type_version_system(major=type_data.get("major", "Major"), minor=type_data.get("minor", "Minor"), patch=type_data.get("patch", "Patch"))

        version_data = data.get("__version", {})
        self.___major = version_data.get(self.___typeVersionSystem.major, 1)
        self.___minor = version_data.get(self.___typeVersionSystem.minor, 0)
        self.___patch = version_data.get(self.___typeVersionSystem.patch, 0)

        self.___history = data.get("history", [])
 
    def ___save_to_json(self) -> None:
        """
        Saves the current state of the version system and project to a JSON file.
        """
        data = {
            "version": self.version(),
            "project": self.___project.__dict__(),
            "history": self.___history,
             "__type": self.___typeVersionSystem.__dict__(),
             "__version": self.__dict__(),
        }
        with open(self.___filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def ___log_change(self, change_type:str, description: str='') -> None:
        f"""
        Records a change in the change history.

        :param change_type: Type of change ({self.___major}, {self.___minor}, {self.___patch}).
        :param description: Descrição da mudança.
        """
        version = f"{self.___major}.{self.___minor}.{self.___patch}"
        self.___history.append({
            "version": version,
            "type": change_type,
            "description": description,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        self.___save_to_json()

    def __increment_patch(self, description: str='') -> None:
        f"""
        Increments the {self.___typeVersionSystem.patch} number and records the change.

        :param description: Description of the reason for the increment.
        """
        self.___patch += 1
        self.___log_change(self.___typeVersionSystem.patch, description)

    def __increment_minor(self, description: str='') -> None:
        """
        Increase the minor number and restart the Patch.
        :param description: Description of the reason for the increment.
        """
        self.___minor += 1
        self.___patch = 0
        self.___log_change(self.___typeVersionSystem.minor, description)

    def __increment_major(self, description: str='') -> None:
        """
        Increments the major number and resets minor and patch.

        :param description: Description of the reason for the increment.
        """
        self.___major += 1
        self.___minor = 0
        self.___patch = 0
        self.___log_change(self.___typeVersionSystem.major, description)
    
    def get_types(self) -> list:
        """
        Returns the types of version system.

        :return: List with version system types.
        """
        return [self.___typeVersionSystem.major, self.___typeVersionSystem.minor, self.___typeVersionSystem.patch]

    def view_info(self) -> None:
        """
        Displays the current version and project information.
        """
        print(self.___info())

    def next(self, type:str, description:str='') -> None:
        """
        Sets a new version.

        :param major: Major version number.
        :param minor: Minor version number.
        :param patch: Patch version number.
        :param description: Description of the reason for the change.
        """
        try:
            type = type.title()
            if type == self.___typeVersionSystem.patch:
                self.__increment_patch(description)
            elif type ==  self.___typeVersionSystem.minor:
                self.__increment_minor(description)
            elif type == self.___typeVersionSystem.major:
                self.__increment_major(description)
        except ValueError:
            raise ValueError("Invalid version type.")
        except Exception as e:
            raise Exception(f"Error setting version.")
        
    def undo_last_change(self) -> None:
        """
        Undo the last change.
        """
        try:
            if len(self.___history) == 0:
                raise ValueError("No changes to undo.")
            
            last_change = self.___history.pop()
            version = last_change["version"]
            major, minor, patch = version.split(".")
            major, minor, patch = int(major), int(minor), int(patch)

            self.___major = major
            self.___minor = minor
            self.___patch = patch

            self.___save_to_json()

        except ValueError as ve:
            raise ve
        except Exception as e:
            raise Exception(f"Error undoing last change.")
        
    def rollback(self, version:str) -> None:
        """
        Returns to a previous version.

        :param version: Version to return.
        """
        try:
            major, minor, patch = version.split(".")
            major, minor, patch = int(major), int(minor), int(patch)

            if major < self.___major:
                self.___major = major
                self.___minor = minor
                self.___patch = patch
            elif minor < self.___minor:
                self.___minor = minor
                self.___patch = patch
            elif patch < self.___patch:
                self.___patch = patch
            else:
                raise ValueError("It is not possible to return to a future version.")

            self.___log_change("Rollback", f"Retorno para a versão {version}")
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise Exception(f"Error rolling back version.")

    def version(self) -> str:
        f"""
        Returns the current version.

        :return: String with the current version in the format 0.0.0.
        """
        return f"{self.___major}.{self.___minor}.{self.___patch}"

    def get_history(self) -> list:
        """
        Returns the change history.

        :return: List with version history.
        """
        return self.___history
    
    def view_history(self) -> None:
        """
        Displays change history.
        """
        try:
            print()
            print(f"{Fore.BLUE}{Style.BRIGHT}{'='*50}")
        
            print(f"{'UPDATE HISTORY':^50}")
            print(f"{'='*50}{Style.RESET_ALL}")
            if len(self.___history) == 0:
                print(f"{Fore.YELLOW} {'No updates recorded.'.center(50)}{Style.RESET_ALL}")
            else:
                for change in self.___history:
                    print(
                        f"{Style.BRIGHT}{Fore.CYAN}{change['version']}{Style.RESET_ALL} "
                        f"- {Fore.GREEN}{change['type']}{Style.RESET_ALL}: "
                        f"{Fore.YELLOW}{change['description']}{Style.RESET_ALL} "
                        f"({Fore.MAGENTA}{change['date']}{Style.RESET_ALL})"
                    )
            print(f"{Fore.BLUE}{Style.BRIGHT}{'='*50}{Style.RESET_ALL}")
            print()
        except Exception as e:
            raise Exception(f"Error displaying change history.")
    
    def get_project(self) -> Project:
        """
        Returns the project data.

        :return: data of the project.
        """
        return self.___project
    
    def update(self,typeVersionSystem:TypeVersionSystem, project:Project):
        try:
            if not typeVersionSystem and not project:
                raise ValueError("No data to update.")
 
            update = False
            if typeVersionSystem:
                self.___typeVersionSystem = typeVersionSystem
                update = True
            if project:
                self.___project = project
                update = True
            if update:
                self.___save_to_json()
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise Exception(f"Error updating data.")

class VersionSystemCLI:
    def __init__(self):
        self.version = VersionSystem()
        self.parser = argparse.ArgumentParser(description=f"{Fore.CYAN}CLI for managing version system.{Style.RESET_ALL}")
        self.subparsers = self.parser.add_subparsers(dest="command", help=f"{Fore.YELLOW}Available commands{Style.RESET_ALL}")
        self._setup_commands()

    def _setup_commands(self):
        try:
            self.subparsers.add_parser("info", help=f"{Fore.GREEN}View current version and project info.{Style.RESET_ALL}")
            self.subparsers.add_parser("version", help=f"{Fore.GREEN}View current version.{Style.RESET_ALL}")

            # Subcommand: next
            next_parser = self.subparsers.add_parser("next", help=f"{Fore.GREEN}Set the next version.{Style.RESET_ALL}")
            next_parser.add_argument("type", choices=self.version.get_types(), help=f"{Fore.BLUE}Type of version increment.{Style.RESET_ALL}")
            next_parser.add_argument("description", nargs="?", default="", help=f"{Fore.BLUE}Description of the change.{Style.RESET_ALL}")

            # Subcommand: undo_last_change
            self.subparsers.add_parser("undo_last_change", help=f"{Fore.GREEN}Undo the last change.{Style.RESET_ALL}")

            # Subcommand: rollback
            rollback_parser = self.subparsers.add_parser("rollback", help=f"{Fore.GREEN}Rollback to a specific version.{Style.RESET_ALL}")
            rollback_parser.add_argument("version", help=f"{Fore.BLUE}Version to rollback to (e.g., 1.2.3).{Style.RESET_ALL}")

            # Subcommand: history
            self.subparsers.add_parser("history", help=f"{Fore.GREEN}View change history.{Style.RESET_ALL}")

            # Subcommand: project
            self.subparsers.add_parser("project", help=f"{Fore.GREEN}Get project details.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error setting up commands: {e}{Style.RESET_ALL}")

    def _clear_line(self):
        print("\033[F\033[K", end="")

    def execute(self):
        try:
            args = self.parser.parse_args()
            if args.command == "info":
                self.version.view_info()
            elif args.command == "version":
                print(self.version)
            elif args.command == "next":
                self.version.next(args.type, args.description)
                print(f"{Fore.GREEN}Version updated successfully.{Style.RESET_ALL}")
            elif args.command == "undo_last_change":
                self.version.undo_last_change()
                print(f"{Fore.YELLOW}Last change undone successfully.{Style.RESET_ALL}")
            elif args.command == "rollback":
                self.version.rollback(args.version)
                print(f"{Fore.GREEN}Rolled back to version {args.version} successfully.{Style.RESET_ALL}")
            elif args.command == "history":
                print(f"{Fore.CYAN}Displaying version history...{Style.RESET_ALL}")
                self.version.view_history()
            elif args.command == "project":
                project = self.version.get_project()
                print(f"{Fore.MAGENTA}{project}{Style.RESET_ALL}")
            else:
                self.parser.print_help()
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

