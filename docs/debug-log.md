# Debug Log

Running log of what broke and why, across all 8 weeks. This is the single most
useful artifact in this repo for showing real engineering judgment — keep entries
short and honest, even the dumb mistakes.

Format:

```
Day 1: WSL install failed via Store (network), fixed with --web-download.
Downloaded wrong Docker arch (ARM64 instead of AMD64) - wasted a download.
Git push rejected - GitHub repo had .gitignore/LICENSE already, needed
--allow-unrelated-histories merge. Accidentally pasted PAT into open chat,
revoked immediately, regenerated.
