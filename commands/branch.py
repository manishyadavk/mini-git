from utils.file_manager import (
    list_branches, branch_exists, read_head, current_branch, write_branch_commit
)


def list_all_branches():
    branches = list_branches()

    if not branches:
        print("No branches yet. Commit first to create one.")
        return

    active = current_branch()

    for name in branches:
        marker = "* " if name == active else "  "
        print(f"{marker}{name}")


def create_branch(name):
    if branch_exists(name):
        print(f"Branch '{name}' already exists.")
        return

    commit_id = read_head()

    if commit_id is None:
        print("Cannot create a branch before the first commit.")
        return

    write_branch_commit(name, commit_id)
    print(f"Created branch '{name}' at {commit_id}")
