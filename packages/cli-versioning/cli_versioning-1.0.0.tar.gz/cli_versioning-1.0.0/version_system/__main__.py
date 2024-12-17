from .version_system import VersionSystemCLI

def main():
    cli = VersionSystemCLI()
    cli.execute()

if __name__ == "__main__":
    main()
