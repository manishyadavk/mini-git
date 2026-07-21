import os

from utils.file_manager import store_object, relative_path, load_index, save_index


def add_file(filename):
    if not os.path.exists(filename):
        print(f"File '{filename}' not found.")
        return

    if not os.path.isfile(filename):
        print(f"'{filename}' is not a file.")
        return

    file_hash = store_object(filename)
    rel_path = relative_path(filename)

    index = load_index()
    index[rel_path] = file_hash
    save_index(index)

    print(f"Added '{rel_path}' to staging area.")
