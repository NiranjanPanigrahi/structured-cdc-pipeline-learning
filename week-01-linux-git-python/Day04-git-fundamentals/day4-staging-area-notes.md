# Day 4: Git Fundamentals — Understanding the Staging Area

## The three-state model
- Working directory → Staging area → Repository
- `git add` doesn't save a file — it queues a *snapshot* of it for the next commit
- You can edit a file again after `git add`, and now working dir and staging area disagree

## Proof: staging then editing again
Staged a file, then added a second line without re-staging. `git status` showed
the SAME file listed under both "Changes to be committed" AND "Changes not
staged for commit" at once — proving they're genuinely separate snapshots,
not just a flag on the file.

## git diff vs git diff --staged
- `git diff` → working directory vs staging area
- `git diff --staged` → staging area vs repository
- These showed completely different diffs when the file was in a mixed state

## Real commit
Staged the full file, committed it, verified with `git log --oneline`

## Extra: pager gotcha
`git log` pipes long output through `less` by default — got stuck once,
learned `q` to quit, and `--no-pager` or `| cat` to bypass it entirely.
Noted `--no-pager` preserves branch labels like (HEAD -> main) while
`| cat` strips them, since piping puts git into non-terminal mode.
