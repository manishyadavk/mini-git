import os

def init_repository():
    repo_path = ".mygit"

    if os.path.exists(repo_path):
        print("Repository already initialized.")
        return

    os.makedirs(".mygit/commits")
    os.makedirs(".mygit/staging")
    os.makedirs(".mygit/objects")

    with open(".mygit/HEAD", "w") as head:
        head.write("")

    print("Initialized empty Mini Git repository.")