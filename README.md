# Mini Git

A simplified, educational version control system written in Python, inspired by
Git's internal model.

## Features

- `init` — initialize an empty repository
- `add <file>` — stage a file (supports nested paths, e.g. `src/app.py`)
- `rm <file>` — untrack a file: deletes it from the working directory and
  stages its removal so the next commit no longer includes it
- `commit "<message>"` — commit staged changes
- `status` — show staged / removed / modified / deleted / untracked files
- `log` — show the current branch's commit history, most recent first
- `checkout <commit_id>` — restore the working directory to a given commit
  (detaches HEAD)
- `checkout <branch>` — switch to an existing branch
- `checkout -b <branch>` — create a new branch at the current commit and
  switch to it
- `branch` — list branches (`*` marks the current one)
- `branch <name>` — create a new branch at the current commit without
  switching to it

## How it works

Mini Git stores its data in a hidden `.mygit/` directory:

```
.mygit/
├── HEAD                  # "ref: <branch>" if attached, or a bare commit id if detached
├── refs/
│   └── heads/
│       └── <branch>      # commit id that branch currently points to
├── objects/               # content-addressable blob storage (like Git's blobs)
│   └── <sha256 of file content>
├── staging/
│   └── index.json         # { "relative/path.txt": "<object hash>" }
└── commits/
    └── <commit id>/
        └── metadata.json   # { id, parent, message, timestamp, files: {path: hash} }
```

Every file's content is hashed with SHA-256 and stored once in `.mygit/objects/`,
keyed by that hash. Two files with identical content — even in different
locations, or across different commits — are stored only once, the same
principle Git's blob storage uses for deduplication and integrity checking.

`add` doesn't copy files by filename; it hashes the file's content, stores the
object if it isn't already present, and records `relative/path -> hash` in the
staging index. `rm` stages a removal by writing `null` for that path in the
index instead of a hash, and deletes the file from the working directory.

Each commit is a full snapshot, not just a delta: `commit` merges the parent
commit's file map with the staging index (staged paths override the parent's,
and any path staged as `null` is dropped) and clears the index. This means
`checkout` on any commit restores every file tracked at that point in history,
not just whatever was staged most recently. `checkout` reads a commit's file
map and restores each path from the object store.

### Branches

`HEAD` either names a branch (`ref: <branch>`) or holds a bare commit id
directly (a detached HEAD, same as real Git). A branch is just a file in
`.mygit/refs/heads/<name>` holding the commit id it currently points to.

- `commit` looks at whichever branch `HEAD` is attached to and moves that
  branch's ref forward to the new commit; if `HEAD` is detached, only `HEAD`
  itself moves, and no branch is updated.
- `branch <name>` creates a new ref pointing at the current commit; it does
  not move `HEAD`.
- `checkout <name>` resolves `<name>` against existing branches first — if it
  matches, `HEAD` becomes `ref: <name>` and the branch's tip is restored;
  otherwise `<name>` is treated as a bare commit id and `HEAD` becomes
  detached.
- Every commit records its `parent`, so `log` walks that chain from `HEAD`
  rather than listing every commit ever made — each branch's log only shows
  its own ancestry, and commits made on other branches don't appear.
- `main` isn't a real ref until the first commit is made (mirroring real
  Git) — an empty repo has no branches yet.

## Usage

```bash
cd your-project
python /path/to/mygit.py init

echo "hello" > notes.txt
python /path/to/mygit.py add notes.txt
python /path/to/mygit.py commit "first commit"

python /path/to/mygit.py status
python /path/to/mygit.py log

python /path/to/mygit.py rm notes.txt
python /path/to/mygit.py commit "remove notes.txt"

python /path/to/mygit.py checkout <commit_id>

# branching
python /path/to/mygit.py checkout -b feature
echo "wip" > feature.txt
python /path/to/mygit.py add feature.txt
python /path/to/mygit.py commit "feature work"

python /path/to/mygit.py branch          # list branches, * marks current
python /path/to/mygit.py checkout main   # switch back
```

## Running tests

```bash
cd "mini-git"
python -m pytest
```

## Known limitations / future work

- No merging — branches can diverge but there's no way to combine them back
  together; that's the natural next feature to build on top of this.
- No diff command between two arbitrary commits.
- `checkout` overwrites working files immediately with no confirmation prompt
  and no check for uncommitted changes — use with care.
- No remote repository support.

These are natural next steps but are out of scope for the current version.
