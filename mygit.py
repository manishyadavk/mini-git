import sys

from commands.init import init_repository
from commands.add import add_file
from commands.commit import commit_changes
from commands.log import show_log
from commands.status import show_status
from commands.checkout import checkout_commit

def main():

    if len(sys.argv) < 2:
        print("Usage: python mygit.py <command>")
        return

    command = sys.argv[1]

    # INIT
    if command == "init":
        init_repository()

    # ADD
    elif command == "add":

        if len(sys.argv) < 3:
            print("Usage: python mygit.py add <filename>")
            return

        add_file(sys.argv[2])

    # COMMIT
    elif command == "commit":

        if len(sys.argv) < 3:
            print('Usage: python mygit.py commit "message"')
            return

        commit_changes(sys.argv[2])

    # LOG
    elif command == "log":
        show_log()

    # STATUS
    elif command == "status":
        show_status()

    # CHECKOUT
    elif command == "checkout":

        if len(sys.argv) < 3:
            print("Usage: python mygit.py checkout <commit_id>")
            return

        checkout_commit(sys.argv[2])

    # UNKNOWN COMMAND
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()