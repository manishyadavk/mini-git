import os
import shutil
import json

from utils.hashing import hash_file

OBJECTS_DIR = os.path.join(".mygit", "objects")
STAGING_INDEX = os.path.join(".mygit", "staging", "index.json")
HEADS_DIR = os.path.join(".mygit", "refs", "heads")
HEAD_FILE = os.path.join(".mygit", "HEAD")
DEFAULT_BRANCH = "main"


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


def _read_head_raw():
    if not os.path.exists(HEAD_FILE):
        return ""

    with open(HEAD_FILE, "r") as f:
        return f.read().strip()


def current_branch():
    """The branch HEAD is attached to, or None if HEAD is detached at a commit."""
    raw = _read_head_raw()

    if raw.startswith("ref: "):
        return raw[len("ref: "):]

    return None


def read_head():
    """Resolve HEAD to the commit id it currently points at, following a
    branch ref if HEAD is attached to one, or None if there is no commit yet."""
    raw = _read_head_raw()

    if not raw:
        return None

    if raw.startswith("ref: "):
        return read_branch_commit(raw[len("ref: "):])

    return raw


def read_branch_commit(name):
    branch_path = os.path.join(HEADS_DIR, name)

    if not os.path.exists(branch_path):
        return None

    with open(branch_path, "r") as f:
        commit_id = f.read().strip()

    return commit_id or None


def write_branch_commit(name, commit_id):
    os.makedirs(HEADS_DIR, exist_ok=True)

    with open(os.path.join(HEADS_DIR, name), "w") as f:
        f.write(commit_id)


def branch_exists(name):
    return os.path.exists(os.path.join(HEADS_DIR, name))


def list_branches():
    if not os.path.exists(HEADS_DIR):
        return []

    return sorted(os.listdir(HEADS_DIR))


def set_head_to_branch(name):
    with open(HEAD_FILE, "w") as f:
        f.write(f"ref: {name}")


def set_head_detached(commit_id):
    with open(HEAD_FILE, "w") as f:
        f.write(commit_id)


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
