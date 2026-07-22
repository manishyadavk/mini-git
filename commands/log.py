import os
import json

from utils.file_manager import read_head, current_branch


def _load_commit(commit_id):
    metadata_file = os.path.join(".mygit", "commits", commit_id, "metadata.json")

    if not os.path.exists(metadata_file):
        return None

    with open(metadata_file, "r") as f:
        return json.load(f)


def show_log():

    commit_id = read_head()

    if commit_id is None:
        print("No commits found.")
        return

    branch = current_branch()
    print(f"On branch {branch}" if branch else "HEAD detached")

    # walk parent pointers from HEAD rather than listing every commit ever
    # made, so log only shows the current branch's own ancestry
    while commit_id:
        data = _load_commit(commit_id)

        if data is None:
            break

        print("\n--------------------")
        print(f"Commit ID : {data['id']}")
        print(f"Message   : {data['message']}")
        print(f"Timestamp : {data['timestamp']}")

        commit_id = data.get("parent")
