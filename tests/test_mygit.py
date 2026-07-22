import os

from commands.init import init_repository
from commands.add import add_file
from commands.rm import remove_file
from commands.commit import commit_changes
from commands.checkout import checkout_commit
from commands.status import show_status
from commands.branch import create_branch
from utils.file_manager import (
    OBJECTS_DIR, load_index, head_files, current_branch, list_branches, read_head
)


def write(path, content):
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w") as f:
        f.write(content)


def read(path):
    with open(path) as f:
        return f.read()


def latest_commit_id():
    return read_head()


def test_init_creates_repo_structure(repo):
    init_repository()

    assert os.path.isdir(".mygit/commits")
    assert os.path.isdir(".mygit/staging")
    assert os.path.isdir(".mygit/objects")
    assert os.path.exists(".mygit/HEAD")


def test_add_commit_checkout_roundtrip(repo):
    init_repository()
    write("hello.txt", "hello world")

    add_file("hello.txt")
    commit_changes("initial commit")

    commit_id = latest_commit_id()
    assert commit_id

    os.remove("hello.txt")
    checkout_commit(commit_id)

    assert read("hello.txt") == "hello world"


def test_staging_area_clears_after_commit(repo):
    init_repository()
    write("a.txt", "a")
    write("b.txt", "b")

    add_file("a.txt")
    add_file("b.txt")
    commit_changes("first commit")

    write("c.txt", "c")
    add_file("c.txt")
    commit_changes("second commit")

    second_id = latest_commit_id()
    with open(f".mygit/commits/{second_id}/metadata.json") as f:
        import json
        files = json.load(f)["files"]

    # a commit is a full snapshot: it must still include files from the
    # parent commit, not just what was newly staged this time
    assert set(files.keys()) == {"a.txt", "b.txt", "c.txt"}

    # the staging index itself is still cleared after each commit -- this is
    # the regression check for the original bug where only the last staged
    # file was removed, leaking earlier entries into the next commit's index
    assert load_index() == {}

    # and the snapshot is actually restorable in full, not just the delta
    os.remove("a.txt")
    os.remove("b.txt")
    os.remove("c.txt")
    checkout_commit(second_id)

    assert read("a.txt") == "a"
    assert read("b.txt") == "b"
    assert read("c.txt") == "c"


def test_nested_paths_do_not_collide(repo):
    init_repository()
    write("src/app.py", "print('src')")
    write("lib/app.py", "print('lib')")

    add_file("src/app.py")
    add_file("lib/app.py")
    commit_changes("add both app.py files")

    commit_id = latest_commit_id()

    os.remove("src/app.py")
    os.remove("lib/app.py")
    checkout_commit(commit_id)

    assert read("src/app.py") == "print('src')"
    assert read("lib/app.py") == "print('lib')"


def test_identical_content_dedupes_to_one_object(repo):
    init_repository()
    write("a.txt", "same content")
    write("b.txt", "same content")

    add_file("a.txt")
    add_file("b.txt")
    commit_changes("dedup test")

    objects = os.listdir(OBJECTS_DIR)
    assert len(objects) == 1


def test_status_buckets(repo):
    init_repository()
    write("tracked.txt", "version 1")
    add_file("tracked.txt")
    commit_changes("track file")

    write("tracked.txt", "version 2")
    write("new.txt", "new")

    result = show_status()

    assert "tracked.txt" in result["modified"]
    assert "new.txt" in result["untracked"]
    assert result["staged"] == []
    assert result["deleted"] == []


def test_status_shows_deleted_file(repo):
    init_repository()
    write("gone.txt", "bye")
    add_file("gone.txt")
    commit_changes("add file to delete")

    os.remove("gone.txt")

    result = show_status()

    assert "gone.txt" in result["deleted"]


def test_rm_untracks_a_committed_file(repo):
    init_repository()
    write("keep.txt", "keep")
    write("drop.txt", "drop")
    add_file("keep.txt")
    add_file("drop.txt")
    commit_changes("first commit")
    first_id = latest_commit_id()

    remove_file("drop.txt")

    # rm deletes the working copy immediately
    assert not os.path.exists("drop.txt")

    # and stages the removal, visible in status before the next commit
    result = show_status()
    assert "drop.txt" in result["removed"]

    commit_changes("remove drop.txt")
    second_id = latest_commit_id()

    # the new commit's snapshot no longer tracks the removed file
    assert "drop.txt" not in head_files()
    assert "keep.txt" in head_files()

    # the staging index is clean again after the commit
    assert load_index() == {}

    # history is preserved: the earlier commit still has the file
    os.remove("keep.txt")
    checkout_commit(first_id)
    assert read("drop.txt") == "drop"

    # and checking back out to the later commit removes it again -- checkout
    # must reconcile the working tree, not just add/overwrite files
    checkout_commit(second_id)
    assert not os.path.exists("drop.txt")


def test_rm_on_untracked_file_is_a_no_op(repo):
    init_repository()
    write("mystery.txt", "???")

    remove_file("mystery.txt")

    # untracked file is left alone, nothing gets staged
    assert os.path.exists("mystery.txt")
    assert load_index() == {}


def test_rm_on_staged_but_uncommitted_file(repo):
    init_repository()
    write("new.txt", "brand new")
    add_file("new.txt")

    remove_file("new.txt")

    assert not os.path.exists("new.txt")
    assert load_index() == {"new.txt": None}

    result = show_status()
    assert "new.txt" in result["removed"]
    assert "new.txt" not in result["untracked"]


def test_init_attaches_head_to_main_branch(repo):
    init_repository()

    assert current_branch() == "main"
    # main isn't a real ref until the first commit, mirroring real git
    assert "main" not in list_branches()


def test_first_commit_creates_main_branch_ref(repo):
    init_repository()
    write("a.txt", "a")
    add_file("a.txt")
    commit_changes("first commit")

    assert "main" in list_branches()
    assert current_branch() == "main"


def test_new_branch_starts_from_current_commit(repo):
    init_repository()
    write("a.txt", "a")
    add_file("a.txt")
    commit_changes("first commit")
    first_id = latest_commit_id()

    create_branch("feature")

    assert set(list_branches()) == {"main", "feature"}
    # branch creation alone doesn't move HEAD
    assert current_branch() == "main"

    checkout_commit("feature")
    assert current_branch() == "feature"
    assert latest_commit_id() == first_id


def test_branches_diverge_independently(repo):
    init_repository()
    write("shared.txt", "v1")
    add_file("shared.txt")
    commit_changes("first commit")

    create_branch("feature")
    checkout_commit("feature")

    write("feature_only.txt", "feature work")
    add_file("feature_only.txt")
    commit_changes("feature commit")

    assert os.path.exists("feature_only.txt")
    assert "feature_only.txt" in head_files()

    checkout_commit("main")

    # switching back to main removes files that only exist on feature...
    assert not os.path.exists("feature_only.txt")
    assert "feature_only.txt" not in head_files()
    # ...and main's own history is untouched by feature's commit
    assert "shared.txt" in head_files()


def test_checkout_commit_id_detaches_head(repo):
    init_repository()
    write("a.txt", "a")
    add_file("a.txt")
    commit_changes("first commit")
    first_id = latest_commit_id()

    write("b.txt", "b")
    add_file("b.txt")
    commit_changes("second commit")

    checkout_commit(first_id)

    assert current_branch() is None
    assert latest_commit_id() == first_id

    # committing while detached moves HEAD but does not touch main
    write("c.txt", "c")
    add_file("c.txt")
    commit_changes("detached commit")

    assert current_branch() is None
    from utils.file_manager import read_branch_commit
    assert read_branch_commit("main") != latest_commit_id()


def test_cannot_branch_before_first_commit(repo):
    init_repository()

    create_branch("too-early")

    assert list_branches() == []
