import os
import shutil

def checkout_commit(commit_id):

    commit_path = os.path.join(
        ".mygit",
        "commits",
        commit_id
    )

    if not os.path.exists(commit_path):
        print("Commit not found.")
        return

    for file in os.listdir(commit_path):

        if file == "metadata.json":
            continue

        source = os.path.join(commit_path, file)

        destination = file

        if os.path.isfile(source):
            shutil.copy2(source, destination)

    with open(".mygit/HEAD", "w") as head:
        head.write(commit_id)

    print(f"Checked out commit {commit_id}")