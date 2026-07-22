import os

from utils.file_manager import HEADS_DIR, DEFAULT_BRANCH


def init_repository():
    repo_path = ".mygit"

    if os.path.exists(repo_path):
        print("Repository already initialized.")
        return

    os.makedirs(".mygit/commits")
    os.makedirs(".mygit/staging")
    os.makedirs(".mygit/objects")
    os.makedirs(HEADS_DIR)

    with open(".mygit/HEAD", "w") as head:
        head.write(f"ref: {DEFAULT_BRANCH}")

    print(f"Initialized empty Mini Git repository on branch '{DEFAULT_BRANCH}'.")