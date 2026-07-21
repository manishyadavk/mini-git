import os
import json
import hashlib
from datetime import datetime

from utils.file_manager import load_index, save_index, head_files


def commit_changes(message):

    index = load_index()

    if not index:
        print("Nothing to commit.")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    commit_id = hashlib.sha256(
        (message + timestamp).encode()
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
        "message": message,
        "timestamp": timestamp,
        "files": files
    }

    with open(
        os.path.join(commit_folder, "metadata.json"),
        "w"
    ) as f:
        json.dump(commit_data, f, indent=4)

    with open(".mygit/HEAD", "w") as head:
        head.write(commit_id)

    save_index({})

    print(f"Commit created: {commit_id}")
