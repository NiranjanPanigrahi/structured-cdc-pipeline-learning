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
