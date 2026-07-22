import os
import json
import hashlib
from datetime import datetime

from utils.file_manager import (
    load_index, save_index, head_files, read_head,
    current_branch, write_branch_commit, set_head_detached
)


def commit_changes(message):

    index = load_index()

    if not index:
        print("Nothing to commit.")
        return

    parent_id = read_head()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    commit_id = hashlib.sha256(
        (message + timestamp + (parent_id or "")).encode()
    ).hexdigest()[:8]

    commit_folder = os.path.join(".mygit", "commits", commit_id)
    os.makedirs(commit_folder)

    # a commit is a full snapshot: carry forward every file already tracked
    # by the parent commit, then layer the newly staged changes on top.
    # a None entry means the path was staged for removal (see commands/rm.py)
    # and must be dropped from the snapshot rather than carried forward.
    merged = {**head_files(), **index}
    files = {path: obj_hash for path, obj_hash in merged.items() if obj_hash is not None}

    commit_data = {
        "id": commit_id,
        "parent": parent_id,
        "message": message,
        "timestamp": timestamp,
        "files": files
    }

    with open(
        os.path.join(commit_folder, "metadata.json"),
        "w"
    ) as f:
        json.dump(commit_data, f, indent=4)

    # advance whichever branch HEAD is attached to; a detached HEAD just
    # moves to the new commit without updating any branch
    branch = current_branch()
    if branch:
        write_branch_commit(branch, commit_id)
    else:
        set_head_detached(commit_id)

    save_index({})

    print(f"Commit created: {commit_id}")
