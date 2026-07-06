---
name: dgstack-upgrade
description: Upgrade an installed DG Stack skill pack from GitHub and rerun setup. Use when the user says upgrade dgstack, update dgstack, get latest dgstack, refresh DG Stack, or asks to update the installed skill pack.
---

# DG Stack Upgrade

Upgrade DG Stack and show what changed.

## Steps

1. Detect the install directory:

```bash
if [ -d "$HOME/.dgstack/.git" ]; then
  INSTALL_DIR="$HOME/.dgstack"
elif [ -d "$HOME/.claude/skills/dgstack/.git" ]; then
  INSTALL_DIR="$HOME/.claude/skills/dgstack"
elif [ -L "$HOME/.claude/skills/dgstack" ]; then
  INSTALL_DIR="$(readlink "$HOME/.claude/skills/dgstack")"
elif [ -L "$HOME/.codex/skills/dgstack" ]; then
  INSTALL_DIR="$(readlink "$HOME/.codex/skills/dgstack")"
elif [ -L "$HOME/.claude/skills/dgstack-upgrade" ]; then
  INSTALL_DIR="$(readlink "$HOME/.claude/skills/dgstack-upgrade")"
elif [ -L "$HOME/.codex/skills/dgstack-upgrade" ]; then
  INSTALL_DIR="$(readlink "$HOME/.codex/skills/dgstack-upgrade")"
else
  echo "ERROR: dgstack not found"; exit 1
fi
INSTALL_DIR="$(cd "$INSTALL_DIR" && pwd -P)"
while [ "$INSTALL_DIR" != "/" ] && [ ! -d "$INSTALL_DIR/.git" ]; do
  INSTALL_DIR="$(dirname "$INSTALL_DIR")"
done
if [ ! -d "$INSTALL_DIR/.git" ]; then
  echo "ERROR: dgstack git repo not found"; exit 1
fi
OLD_VERSION=$(cat "$INSTALL_DIR/VERSION" 2>/dev/null | tr -d '[:space:]' || echo "unknown")
echo "INSTALL_DIR=$INSTALL_DIR OLD_VERSION=$OLD_VERSION"
```

2. Pull latest and rerun setup:

```bash
cd "$INSTALL_DIR"
git fetch origin
git reset --hard origin/main
./setup --target both --quiet
NEW_VERSION=$(cat VERSION 2>/dev/null | tr -d '[:space:]' || echo "unknown")
echo "NEW_VERSION=$NEW_VERSION"
```

3. Report the result:

If `OLD_VERSION` equals `NEW_VERSION`, say DG Stack is already current. If a
`CHANGELOG.md` exists, summarize the changes since `OLD_VERSION` in 3-5 bullets.
Otherwise, summarize the latest commit range.
