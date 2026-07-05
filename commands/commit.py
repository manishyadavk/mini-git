import os
import json
import shutil
import hashlib
from datetime import datetime

def commit_changes(message):

    staging_path = ".mygit/staging"

    if not os.listdir(staging_path):
        print("Nothing to commit.")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    commit_id = hashlib.sha256(
        (message + timestamp).encode()
    ).hexdigest()[:8]

    commit_folder = os.path.join(".mygit/commits", commit_id)

    os.makedirs(commit_folder)

    # Copy staged files into commit snapshot
    for file in os.listdir(staging_path):
        source = os.path.join(staging_path, file)
        destination = os.path.join(commit_folder, file)

        if os.path.isfile(source):
            shutil.copy2(source, destination)

    commit_data = {
        "id": commit_id,
        "message": message,
        "timestamp": timestamp
    }

    with open(
        os.path.join(commit_folder, "metadata.json"),
        "w"
    ) as f:
        json.dump(commit_data, f, indent=4)

    with open(".mygit/HEAD", "w") as head:
        head.write(commit_id)

    print(f"Commit created: {commit_id}")

    for file in os.listdir(staging_path):
     file_path = os.path.join(staging_path, file)

    if os.path.isfile(file_path):
        os.remove(file_path)