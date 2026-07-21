import argparse

from commands.init import init_repository
from commands.add import add_file
from commands.rm import remove_file
from commands.commit import commit_changes
from commands.log import show_log
from commands.status import show_status
from commands.checkout import checkout_commit


def build_parser():
    parser = argparse.ArgumentParser(
        prog="mygit",
        description="Mini Git: a simplified version control system."
    )
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("init", help="Initialize an empty repository")

    add_parser = subparsers.add_parser("add", help="Stage a file")
    add_parser.add_argument("filename", help="Path to the file to stage")

    rm_parser = subparsers.add_parser("rm", help="Untrack a file and stage its removal")
    rm_parser.add_argument("filename", help="Path to the file to untrack")

    commit_parser = subparsers.add_parser("commit", help="Commit staged changes")
    commit_parser.add_argument("message", help="Commit message")

    subparsers.add_parser("log", help="Show commit history")
    subparsers.add_parser("status", help="Show staged/modified/untracked files")

    checkout_parser = subparsers.add_parser(
        "checkout", help="Restore files from a commit"
    )
    checkout_parser.add_argument("commit_id", help="Commit ID to check out")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "init":
        init_repository()
    elif args.command == "add":
        add_file(args.filename)
    elif args.command == "rm":
        remove_file(args.filename)
    elif args.command == "commit":
        commit_changes(args.message)
    elif args.command == "log":
        show_log()
    elif args.command == "status":
        show_status()
    elif args.command == "checkout":
        checkout_commit(args.commit_id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
