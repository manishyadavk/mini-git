import os

from utils.file_manager import load_index, relative_path, head_files, current_branch
from utils.hashing import hash_file

IGNORED_DIRS = {".mygit", ".git", "__pycache__"}


def _working_tree_files():
    files = {}

    for root, dirs, filenames in os.walk("."):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

        for filename in filenames:
            path = os.path.join(root, filename)
            files[relative_path(path)] = path

    return files


def show_status():

    empty_result = {
        "staged": [], "modified": [], "untracked": [], "deleted": [], "removed": []
    }

    if not os.path.exists(".mygit"):
        print("Repository not initialized.")
        return empty_result

    branch = current_branch()
    print(f"On branch {branch}" if branch else "HEAD detached")

    staged = load_index()
    committed = head_files()
    working = _working_tree_files()

    result = {k: [] for k in empty_result}

    for rel_path, obj_hash in sorted(staged.items()):
        if obj_hash is None:
            result["removed"].append(rel_path)

    for rel_path, disk_path in sorted(working.items()):
        if rel_path in staged and staged[rel_path] is None:
            continue

        current_hash = hash_file(disk_path)
        staged_hash = staged.get(rel_path)
        committed_hash = committed.get(rel_path)

        if staged_hash == current_hash:
            result["staged"].append(rel_path)
        elif committed_hash == current_hash and rel_path not in staged:
            continue
        elif staged_hash is not None or committed_hash is not None:
            result["modified"].append(rel_path)
        else:
            result["untracked"].append(rel_path)

    for rel_path in sorted(committed):
        if rel_path not in working and rel_path not in staged:
            result["deleted"].append(rel_path)

    if result["staged"]:
        print("Staged files:")
        for path in result["staged"]:
            print(f"  {path}")

    if result["removed"]:
        print("Removed files (staged for deletion):")
        for path in result["removed"]:
            print(f"  {path}")

    if result["modified"]:
        print("Modified files (not staged):")
        for path in result["modified"]:
            print(f"  {path}")

    if result["deleted"]:
        print("Deleted files (not staged):")
        for path in result["deleted"]:
            print(f"  {path}")

    if result["untracked"]:
        print("Untracked files:")
        for path in result["untracked"]:
            print(f"  {path}")

    if not any(result.values()):
        print("Nothing to commit, working tree clean.")

    return result
