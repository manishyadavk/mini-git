import os
import shutil

def add_file(filename):
    if not os.path.exists(filename):
        print(f"File '{filename}' not found.")
        return

    staging_path = os.path.join(".mygit", "staging")

    shutil.copy2(filename, staging_path)

    print(f"Added '{filename}' to staging area.")