import os
import json

from utils.file_manager import (
    restore_object, head_files, branch_exists, read_branch_commit,
    set_head_to_branch, set_head_detached
)


def _load_commit(commit_id):
    metadata_path = os.path.join(".mygit", "commits", commit_id, "metadata.json")

    if not os.path.exists(metadata_path):
        return None

    with open(metadata_path, "r") as f:
        return json.load(f)


def checkout_commit(target):

    # a target that names an existing branch checks out that branch's tip
    # and leaves HEAD attached to it; anything else is treated as a bare
    # commit id and leaves HEAD detached, mirroring real git's behavior
    is_branch = branch_exists(target)

    if is_branch:
        commit_id = read_branch_commit(target)
        if commit_id is None:
            print(f"Branch '{target}' has no commits yet.")
            return
    else:
        commit_id = target

    commit_data = _load_commit(commit_id)

    if commit_data is None:
        print("Commit not found.")
        return

    target_files = commit_data["files"]

    # remove files that the current commit tracks but the target commit
    # doesn't, so checkout actually reconciles the working tree to match the
    # target snapshot rather than only ever adding/overwriting files
    for rel_path in head_files():
        if rel_path not in target_files and os.path.isfile(rel_path):
            os.remove(rel_path)

    for rel_path, file_hash in target_files.items():
        restore_object(file_hash, rel_path)

    if is_branch:
        set_head_to_branch(target)
        print(f"Switched to branch '{target}'")
    else:
        set_head_detached(commit_id)
        print(f"Checked out commit {commit_id} (detached HEAD)")
