# Hotfix Workflow

Emergency patch release process for critical fixes.

## When to Use

- Security vulnerabilities
- Critical bugs in production
- Data corruption issues
- Service outages

## Quick Hotfix (Minimal Steps)

```bash
# 1. Create hotfix branch
git checkout -b hotfix/security-patch

# 2. Make critical fix
# ... edit files ...

# 3. Fast commit without tests
goal push --yes --no-test \
  -m "hotfix: patch CVE-2024-XXXX"

# 4. Fast-forward to main
git checkout main
git merge --ff-only hotfix/security-patch
git push origin main

# 5. Tag and push (already done by goal)
```

## Proper Hotfix with Tests

```bash
# 1. Create hotfix branch
git checkout -b hotfix/critical-fix

# 2. Fix and add tests
# ... edit + tests ...

# 3. Stage and commit
git add .
goal push --yes -m "hotfix: resolve critical issue"

# 4. Merge to main
git checkout main
git merge hotfix/critical-fix --no-ff
git push origin main

# 5. Proper release
goal push --bump patch --yes \
  -m "release: v1.2.1 with security fix"
```

## Skip Unnecessary Steps

| Flag | Effect | When to Use |
|------|--------|-------------|
| `--no-test` | Skip tests | Verified locally |
| `--no-tag` | Skip git tag | Will tag manually |
| `--no-changelog` | Skip changelog | Hotfix too minor |
| `--no-version-sync` | Skip version bump | Same version |
| `--no-publish` | Skip registry | Internal only |

## Example: Security Patch

```bash
# Critical security fix
git checkout -b hotfix/cve-2024-1234

# Apply patch from security team
patch -p1 < security-fix.patch

# Commit immediately
goal push --yes --no-test --no-changelog \
  --bump patch \
  -m "hotfix: patch CVE-2024-1234 (critical)"

# Merge fast
git checkout main
git merge --ff hotfix/cve-2024-1234
git push origin main --tags

# Notify team
slack-post "#deploys" "Security patch deployed: v1.2.1"
```

## Recovery

If hotfix fails:

```bash
# Revert
git revert HEAD
goal push --yes -m "revert: undo failed hotfix"

# Re-apply with fix
git cherry-pick <commit> --no-commit
# ... fix issues ...
goal push --yes -m "hotfix: corrected patch"
```

## See Also

- [Feature Branch Workflow](feature-branch.md)
- [Release Candidates](release-candidate.md)
