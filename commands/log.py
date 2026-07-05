import os
import json

def show_log():

    commits_path = ".mygit/commits"

    if not os.path.exists(commits_path):
        print("No commits found.")
        return

    commits = os.listdir(commits_path)

    if not commits:
        print("No commits found.")
        return

    for commit_id in sorted(commits, reverse=True):

        metadata_file = os.path.join(
            commits_path,
            commit_id,
            "metadata.json"
        )

        if os.path.exists(metadata_file):

            with open(metadata_file, "r") as f:
                data = json.load(f)

            print("\n--------------------")
            print(f"Commit ID : {data['id']}")
            print(f"Message   : {data['message']}")
            print(f"Timestamp : {data['timestamp']}")