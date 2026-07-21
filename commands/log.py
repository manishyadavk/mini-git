import os
import json


def show_log():

    commits_path = ".mygit/commits"

    if not os.path.exists(commits_path):
        print("No commits found.")
        return

    commit_ids = os.listdir(commits_path)

    if not commit_ids:
        print("No commits found.")
        return

    commits = []

    for commit_id in commit_ids:

        metadata_file = os.path.join(
            commits_path,
            commit_id,
            "metadata.json"
        )

        if os.path.exists(metadata_file):
            with open(metadata_file, "r") as f:
                commits.append(json.load(f))

    # commit ids are a hash of message+timestamp, so sorting by id is not
    # chronological -- sort by the recorded timestamp instead.
    commits.sort(key=lambda c: c["timestamp"], reverse=True)

    for data in commits:
        print("\n--------------------")
        print(f"Commit ID : {data['id']}")
        print(f"Message   : {data['message']}")
        print(f"Timestamp : {data['timestamp']}")
