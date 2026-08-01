## [Week 1, Day 1] — WSL2 install blocked by network/Store connectivity

**What broke:** `wsl --install` and `wsl.exe --install` both failed repeatedly with
"A connection with the server could not be established" — WSL wasn't installed
at all yet at this point.

**Why I thought it broke (at the time):** Assumed it was a Docker Desktop issue
at first, since I'd been troubleshooting Docker separately. Took a moment to
realize this was happening at the WSL install step itself, before Docker was
even involved.


**Actual root cause:** The standard `wsl --install` command pulls the Linux
kernel and Ubuntu image through the Microsoft Store backend, which was being
blocked or failing on my network — general internet access (ping google.com)
worked fine, so it was a selective/Store-specific connectivity issue, not a
broader outage.

**Fix:** Used `wsl --install -d Ubuntu --web-download`, which downloads directly
instead of going through the Store. Also manually installed the WSL kernel
update (`.msi`) as a fallback path before this worked.

**Time lost:** ~1-2 hours across multiple retry attempts.

---

## [Week 1, Day 1] — Downloaded wrong Docker Desktop architecture

**What broke:** Downloaded and tried to install "Docker Desktop for ARM64,"
which failed/wouldn't run correctly.

**Why I thought it broke:** Confused "AMD64" naming with the AMD *brand* —
assumed since my CPU is Intel, I needed a different build (ARM64) instead.

**Actual root cause:** AMD64 is the name of the standard 64-bit architecture
used by both Intel and AMD processors (AMD originally designed the extension,
hence the name) — it has nothing to do with CPU brand. ARM64 is the genuinely
different architecture, used in phones and ARM-based laptops, which my Intel
i3-1215U is not.

**Fix:** Re-downloaded the correct AMD64 build and installed that instead.

**Time lost:** ~15-20 minutes.

---

## [Week 1, Day 1] — git push rejected due to divergent histories

**What broke:** `git push -u origin main` was rejected with
"Updates were rejected because the remote contains work that you do not have
locally."

**Why I thought it broke:** Assumed something had gone wrong with my local
commit.

**Actual root cause:** The GitHub repo was created with a `.gitignore` and
`LICENSE` file already in it (via GitHub's UI), while my local repo was
initialized separately and had no knowledge of those files — two genuinely
unrelated commit histories trying to push to the same branch.

**Fix:** `git pull origin main --allow-unrelated-histories --no-rebase`,
resolved the merge commit message in nano (`Ctrl+X` → `Y` → `Enter`), then
pushed successfully.

**Time lost:** ~20-30 minutes, including one detour where old terminal output
text got accidentally pasted back into the terminal and interpreted as
commands — harmless, but confusing until I recognized what had happened.

---

## [Week 1, Day 1] — Accidentally exposed a Personal Access Token

**What broke:** Pasted a freshly generated GitHub Personal Access Token
directly into the chat while asking for help, rather than only into the
terminal's password prompt.

**Why this matters:** A PAT pasted anywhere outside a terminal's password
field should be treated as compromised, even if nothing malicious happens
with it — it's a credential, same category of sensitivity as a password.

**Fix:** Deleted the token immediately via GitHub → Settings → Developer
settings → Personal access tokens, then generated a fresh one and used it
correctly (pasted only into the terminal prompt, never elsewhere).

**Time lost:** ~5 minutes, no lasting impact since it was caught and revoked
right away.

Day 1: WSL install failed via Store (network), fixed with --web-download.
Downloaded wrong Docker arch (ARM64 instead of AMD64) - wasted a download.
Git push rejected - GitHub repo had .gitignore/LICENSE already, needed
--allow-unrelated-histories merge. Accidentally pasted PAT into open chat,
revoked immediately, regenerated.
 7c4bffe7aa90b137af240adab31ca6047d748376

## [Week 1, Day 2] — `mkdir` created a directory instead of a file

**What broke:** Ran `mkdir test.sh` intending to create an empty file to
practice `chmod` on, then tried to `cd` into it expecting to edit it.

**Why I thought it broke:** Assumed the `.sh` extension would make `mkdir`
treat it as a file, or that I'd just made a typo somewhere.

**Actual root cause:** `mkdir` always creates a directory, regardless of
the name given to it — a file extension like `.sh` is purely a naming
convention for humans (and some tools), it has no effect on what `mkdir`
actually does.

**Fix:** `rmdir test.sh` to remove the empty directory, then `touch test.sh`
to actually create it as a file, before continuing with the `chmod` drill.

**Time lost:** ~2 minutes.

---

## [Week 1, Day 3] — WSL2 ↔ Docker Desktop integration silently broke

**What broke:** `docker compose up -d` failed with
`/usr/bin/docker: Input/output error`. Later in the same day, after a
restart, `docker` commands failed again with
`The command 'docker' could not be found in this WSL 2 distro`, even
though Docker Desktop's own GUI showed the engine running normally.

**Why I thought it broke:** Assumed Docker Desktop itself was unhealthy,
or that the WSL Integration toggle in Docker Desktop's settings had been
switched off.

**Actual root cause:** Traced it with `which docker`, `ls -la /usr/bin/docker`,
and `ls -la /mnt/wsl/`. Found that `/usr/bin/docker` is a symlink pointing to
`/mnt/wsl/docker-desktop/cli-tools/usr/bin/docker` — a path that Docker
Desktop creates dynamically when its WSL2 integration mount is healthy.
That directory didn't exist at all, meaning the integration mount itself
had failed to attach, not the Docker engine.

**Fix:** Fully quit Docker Desktop (not just close the window — used the
system tray icon's "Quit Docker Desktop"), ran `wsl --shutdown` from
PowerShell, waited, then relaunched Docker Desktop fresh. Confirmed with
`ls -la /mnt/wsl/` that `docker-desktop` reappeared, then `docker ps`
worked correctly from WSL again.

**Time lost:** ~45-60 minutes, including one dead-end checking the WSL
Integration toggle (which was already correctly enabled the whole time).

---

## [Week 1, Day 3] — `sed` preview mode mistaken for an actual file edit

**What broke:** Ran `sed 's/ERROR/CRITICAL/' sample.log`, saw the
substituted text printed correctly in the terminal, and assumed the file
itself had been updated. A follow-up `grep -i critical sample.log`
returned nothing.

**Why I thought it broke:** Assumed `grep` was somehow failing to match
text that was clearly visible moments earlier in the terminal.

**Actual root cause:** `sed` without the `-i` flag never modifies the
original file — it only prints a preview of what the substitution would
look like. The terminal output was real, but it was never written back
to disk, so the file on disk still said `ERROR` the whole time.

**Fix:** Committed the file to git first as a safety baseline, then re-ran
the same substitution with `sed -i 's/ERROR/CRITICAL/' sample.log`, which
edits in place. Confirmed the change stuck with `grep -i critical`
afterward.

**Time lost:** ~10 minutes, mostly spent confused about why `grep` "wasn't
working" before realizing the file was never actually touched.

---

## [Week 1, Day 3] — `.gitignore`'s `*.log` rule silently excluded a practice file

**What broke:** Created `sample.log` for a `grep`/`awk`/`sed` exercise,
then later ran `git status` expecting to see it as untracked — instead
got "nothing to commit, working tree clean," as if the file didn't exist
to git at all.

**Why I thought it broke:** Assumed the file had somehow already been
committed in an earlier session I didn't remember, or that something
was wrong with git itself.

**Actual root cause:** Checked `git log --oneline -- sample.log` (empty —
never committed) and then `cat .gitignore`, which contained a standard
Python-template line, `*.log`, meant for framework log files — but it
matches *any* file ending in `.log`, anywhere in the repo, with no
awareness of intent. It was silently telling git to ignore the practice
file entirely.

**Fix:** Renamed the file from `sample.log` to `sample-cdc-pipeline.log.txt`
so it no longer matches the `*.log` wildcard, confirmed with `git status`
that it now showed as untracked, then added/committed/pushed normally.

**Time lost:** ~10-15 minutes tracing it back to the `.gitignore` rule.

## [Week 1, Day 3] — grep typo silently produced an empty file
**What broke:** Ran `grep -i "critial" sample-cdc-pipeline.log.txt >
criteria1-critical-events.txt` — misspelled "critical." `cat` on the output
file showed nothing.
**Why I thought it broke:** Assumed grep or the redirect had failed outright.
**Actual root cause:** Grep ran fine and correctly found zero matches for
the (misspelled) pattern. `>` still creates the output file regardless of
whether grep matches anything — an empty result is not the same as an error.
**Fix:** Re-ran with correct spelling ("critical"), confirmed 2 CRITICAL
lines in the output.
**Time lost:** ~5 minutes.

---

## [Week 1, Day 3] — Unclosed quote left the terminal hanging
**What broke:** Started a command with `"kafka-producer-events.txt` and
never closed the quote — terminal just sat there waiting, no prompt.
**Why I thought it broke:** Looked like the terminal had frozen.
**Actual root cause:** Bash was still waiting for the closing `"` before it
would treat the command as complete — this is expected behavior, not a bug.
**Fix:** `Ctrl+C` to cancel and get a fresh prompt, then re-typed the full
command with matched quotes.
**Time lost:** <1 minute once recognized.

---

## [Week 1, Day 4] — `mkdir` created a directory instead of a file
**What broke:** Ran `mkdir servers.log` intending to create a log *file* —
`mkdir` always creates directories regardless of what the name looks like.
Ended up `cd`'d into an empty directory named `servers.log`, then couldn't
`rm` it (wrong location, then `rm` refused since it was a directory).
**Why I thought it broke:** Assumed the `.log` extension would signal file
type to the command — it doesn't. Extensions are naming convention only,
not enforced by the shell or filesystem.
**Actual root cause:** Used `mkdir` when the goal was file creation.
`mkdir` = make directory, always. File creation needs `touch`, `nano`, or
`cat >`.
**Fix:** `rmdir servers.log` (safe since it was empty) from the parent
directory, then recreated it correctly as a file.
**Time lost:** ~2 minutes, no data lost.

---

## [Week 1, Day 4] — Heredoc paste didn't work as one block
**What broke:** Tried `cat > servers.log << 'EOF' ... EOF` to write
multi-line content in one shot. Terminal didn't paste it as a single
atomic command — a stray file literally named `EOF` got created with the
heredoc body as its content, since bash lost track of the redirect once
the multi-line paste got split across separate lines.
**Why I thought it broke:** Assumed heredocs would always paste cleanly
regardless of terminal.
**Actual root cause:** Windows Terminal/WSL doesn't always paste multi-line
input as one atomic block — each line can get sent separately, breaking
the `<<` redirect mid-command.
**Fix:** Fell back to `nano servers.log` and typed content directly instead
of relying on heredoc paste in this terminal.
**Time lost:** ~3 minutes, cleaned up with `rm EOF`.

---

## [Week 1, Day 4] — `git log` pager garbled the screen
**What broke:** `git log --oneline -100` piped into `less` (git's default
pager for long output). Arrow key / scroll input got interpreted as escape
sequences, scrambling the redraw into repeated garbage blocks (`ESCOC`,
`ESCOD`, etc.).
**Why I thought it broke:** Looked like git itself had glitched or the
terminal had corrupted output.
**Actual root cause:** Normal `less` pager behavior reacting to unexpected
key input — nothing was actually broken, just visually messy.
**Fix:** `q` quits the pager cleanly. `--no-pager` or `| cat` avoids
launching the pager at all — worth noting `--no-pager` preserves branch
labels like `(HEAD -> main)` while `| cat` strips them, since piping puts
git into non-terminal output mode.
**Time lost:** <1 minute once recognized.
