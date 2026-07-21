import os
import json

from utils.file_manager import restore_object, head_files


def checkout_commit(commit_id):

    commit_path = os.path.join(".mygit", "commits", commit_id)
    metadata_path = os.path.join(commit_path, "metadata.json")

    if not os.path.exists(metadata_path):
        print("Commit not found.")
        return

    with open(metadata_path, "r") as f:
        commit_data = json.load(f)

    target_files = commit_data["files"]

    # remove files that the current commit tracks but the target commit
    # doesn't, so checkout actually reconciles the working tree to match the
    # target snapshot rather than only ever adding/overwriting files
    for rel_path in head_files():
        if rel_path not in target_files and os.path.isfile(rel_path):
            os.remove(rel_path)

    for rel_path, file_hash in target_files.items():
        restore_object(file_hash, rel_path)

    with open(".mygit/HEAD", "w") as head:
        head.write(commit_id)

    print(f"Checked out commit {commit_id}")
