import os

from utils.file_manager import load_index, save_index, head_files, relative_path


def remove_file(filename):
    rel_path = relative_path(filename)

    index = load_index()
    tracked = head_files()

    if rel_path not in index and rel_path not in tracked:
        print(f"'{rel_path}' is not tracked.")
        return

    # a None value marks the path for deletion on the next commit
    index[rel_path] = None
    save_index(index)

    if os.path.isfile(filename):
        os.remove(filename)

    print(f"Removed '{rel_path}' from tracking.")
