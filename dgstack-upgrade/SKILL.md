---
name: dgstack-upgrade
version: 0.1.0
description: Upgrade dgstack to the latest version from GitHub.
triggers:
  - upgrade dgstack
  - update dgstack
  - get latest dgstack
allowed-tools:
  - Bash
  - Read
---

# /dgstack-upgrade

Upgrade dgstack and show what changed.

## Steps

### 1. Detect install

```bash
if [ -d "$HOME/.claude/skills/dgstack/.git" ]; then
  INSTALL_DIR="$HOME/.claude/skills/dgstack"
elif [ -L "$HOME/.claude/skills/dgstack" ]; then
  INSTALL_DIR="$(readlink "$HOME/.claude/skills/dgstack")"
else
  echo "ERROR: dgstack not found"; exit 1
fi
INSTALL_DIR="$(cd "$INSTALL_DIR" && pwd -P)"
OLD_VERSION=$(cat "$INSTALL_DIR/VERSION" 2>/dev/null | tr -d '[:space:]' || echo "unknown")
echo "INSTALL_DIR=$INSTALL_DIR  OLD_VERSION=$OLD_VERSION"
```

### 2. Pull latest

```bash
cd "$INSTALL_DIR"
git fetch origin
git reset --hard origin/main
./setup --quiet
NEW_VERSION=$(cat VERSION | tr -d '[:space:]')
echo "NEW_VERSION=$NEW_VERSION"
```

If `OLD_VERSION == NEW_VERSION`, tell the user they're already on the latest version and stop.

### 3. Report

Read `$INSTALL_DIR/CHANGELOG.md` if present and summarize changes since `$OLD_VERSION` in 3-5 bullets.

Format:
```
dgstack v{new} — upgraded from v{old}!
- bullet 1
- bullet 2
```
