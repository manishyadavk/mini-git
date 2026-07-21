import os
import shutil
import json

from utils.hashing import hash_file

OBJECTS_DIR = os.path.join(".mygit", "objects")
STAGING_INDEX = os.path.join(".mygit", "staging", "index.json")


def relative_path(filename):
    return os.path.relpath(filename).replace(os.sep, "/")


def store_object(filepath):
    file_hash = hash_file(filepath)
    object_path = os.path.join(OBJECTS_DIR, file_hash)

    if not os.path.exists(object_path):
        os.makedirs(OBJECTS_DIR, exist_ok=True)
        shutil.copy2(filepath, object_path)

    return file_hash


def restore_object(file_hash, dest_path):
    object_path = os.path.join(OBJECTS_DIR, file_hash)

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    shutil.copy2(object_path, dest_path)


def load_index():
    if not os.path.exists(STAGING_INDEX):
        return {}

    with open(STAGING_INDEX, "r") as f:
        return json.load(f)


def save_index(index):
    with open(STAGING_INDEX, "w") as f:
        json.dump(index, f, indent=4)


def read_head():
    head_path = os.path.join(".mygit", "HEAD")

    if not os.path.exists(head_path):
        return None

    with open(head_path, "r") as f:
        commit_id = f.read().strip()

    return commit_id or None


def load_commit_files(commit_id):
    if commit_id is None:
        return {}

    metadata_path = os.path.join(".mygit", "commits", commit_id, "metadata.json")

    if not os.path.exists(metadata_path):
        return {}

    with open(metadata_path, "r") as f:
        return json.load(f).get("files", {})


def head_files():
    return load_commit_files(read_head())
