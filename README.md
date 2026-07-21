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
- `log` — show commit history, most recent first
- `checkout <commit_id>` — restore the working directory to a given commit

## How it works

Mini Git stores its data in a hidden `.mygit/` directory:

```
.mygit/
├── HEAD                 # commit id currently checked out
├── objects/              # content-addressable blob storage (like Git's blobs)
│   └── <sha256 of file content>
├── staging/
│   └── index.json        # { "relative/path.txt": "<object hash>" }
└── commits/
    └── <commit id>/
        └── metadata.json  # { id, message, timestamp, files: {path: hash} }
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
```

## Running tests

```bash
cd "mini-git"
python -m pytest
```

## Known limitations / future work

- No branching or merging — history is a single linear sequence of commits.
- No diff command between two arbitrary commits.
- `checkout` overwrites working files immediately with no confirmation prompt
  and no check for uncommitted changes — use with care.
- No remote repository support.

These are natural next steps but are out of scope for the current version.
