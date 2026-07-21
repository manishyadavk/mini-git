# Mini Git — Live Demo Script

A rehearsed walkthrough that touches every command and every behavior worth
showing off: staging, full-snapshot commits, status diffing, content
deduplication, untracking a file, and time-travel via checkout.

## Before you start

Reset the demo project to a clean, un-initialized state (safe to re-run
anytime while rehearsing):

```bash
bash "$HOME/mini-git/demo/setup_demo.sh"
```

Then set up a shortcut for the session and move into the demo project:

```bash
alias mygit='python3 "$HOME/mini-git/mygit.py"'
cd "$HOME/mini-git-demo-project"
```

You now have a small "blog" project: `index.html`, `style.css`, `src/app.py`
— none of it tracked yet.

---

## Step 1 — Initialize the repository

```bash
mygit init
```
**Say:** "This creates a hidden `.mygit/` folder — that's where all history
and file content will live, completely separate from the project files."

## Step 2 — See what's untracked

```bash
mygit status
```
**Expect:** all three files listed under "Untracked files". **Say:** "status
compares the working directory against what's actually committed — right
now nothing is, so everything shows as untracked."

## Step 3 — Stage files (including a nested path)

```bash
mygit add index.html
mygit add style.css
mygit add src/app.py
mygit status
```
**Expect:** all three now under "Staged files". **Say:** "add works with
nested paths — `src/app.py` is tracked by its full relative path, not just
the bare filename, so two files named the same thing in different folders
never collide."

## Step 4 — First commit

```bash
mygit commit "Initial project setup"
mygit log
```
**Say:** "Each commit is a full snapshot of every tracked file at that
point, not just a diff — that matters later."

## Step 5 — Modify a file, see it flagged

```bash
echo "  <p>Post 1: Hello world</p>" >> index.html
mygit status
```
**Expect:** `index.html` under "Modified files (not staged)". **Say:**
"status hashes the working copy and compares it to what's committed — since
the content changed, it shows up as modified, not staged."

```bash
mygit add index.html
mygit commit "Add first blog post"
```

## Step 6 — Deduplication via content-addressable storage

```bash
cp src/app.py config_backup.py
mygit add config_backup.py
mygit commit "Add a backup copy of app.py"
ls .mygit/objects | wc -l
```
**Say:** "`config_backup.py` is byte-for-byte identical to `src/app.py`.
Mini Git hashes file *content* with SHA-256 — identical content is stored
once in `.mygit/objects/`, no matter how many files or commits reference it.
That's the same principle Git's blob storage uses." (Object count should be
**4, not 5** — by this point there are 4 distinct contents ever committed
(`index.html` v1, `index.html` v2, `style.css`, `app.py`); `config_backup.py`
reuses `app.py`'s object instead of creating a 5th.)

## Step 7 — Untrack a file

```bash
mygit rm style.css
mygit status
```
**Expect:** `style.css` gone from disk, shown under "Removed files (staged
for deletion)". **Say:** "rm deletes the working copy and stages the
removal — the next commit will no longer include it, but it's not gone from
history."

```bash
mygit commit "Remove unused stylesheet"
mygit log
```
**Say:** "Four commits now, newest first."

## Step 8 — Time travel

```bash
mygit log
```
Copy the commit ID of **"Initial project setup"** (the oldest one) from the
output, then:

```bash
mygit checkout <that_commit_id>
ls
cat style.css
```
**Expect:** `style.css` is back, and `index.html`/`config_backup.py` reflect
their state from that early commit. **Say:** "checkout restores the working
directory to exactly what it looked like at that commit."

Now return to the present — copy the ID of **"Remove unused stylesheet"**
(the newest one):

```bash
mygit checkout <newest_commit_id>
ls
```
**Expect:** `style.css` is gone again. **Say:** "checkout doesn't just add
files back, it reconciles the whole working tree to match the target
snapshot — so going forward again correctly removes files that shouldn't be
there anymore."

## Step 9 — Clean status, and the test suite

```bash
mygit status
```
**Expect:** "Nothing to commit, working tree clean."

```bash
cd "$HOME/mini-git"
python3 -m pytest -v
```
**Say:** "And this is the automated test suite covering all of this —
staging, commits, checkout, deduplication, and status — so it's not just
this one manual run, it's verified automatically."

---

## If something looks off mid-demo

- Re-run `bash demo/setup_demo.sh` before your next rehearsal to reset the
  demo project from scratch — it's idempotent.
- Commit IDs are generated from the message + timestamp, so they'll be
  different every time you run this — always read them from `mygit log`,
  never hardcode one.
