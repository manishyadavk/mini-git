import os

def show_status():

    staging_path = ".mygit/staging"

    if not os.path.exists(staging_path):
        print("Repository not initialized.")
        return

    files = os.listdir(staging_path)

    if not files:
        print("No files staged.")
        return

    print("Staged Files:")

    for file in files:
        print(f"- {file}")