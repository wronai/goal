# Multi-Author Project Example

This example demonstrates how to use Goal's multi-author features for team collaboration.

## Quick Start

```bash
# Clone this example
git clone https://github.com/wronai/goal.git
cd goal/examples/multi-author

# Add team members
python3 -m goal authors add "Alice Chen" alice@company.com --role "Lead Developer"
python3 -m goal authors add Bob bob@company.com --role "Designer"

# Make a commit with co-authors
python3 -m goal commit --co-author "Alice Chen <alice@company.com>"
```

## Managing Authors

### Adding Authors

```bash
# Add with role
goal authors add "Alice Chen" alice@company.com --role "Lead Developer"

# Add with alias for quick reference
goal authors add "Bob Smith" bob@company.com --alias "bob" --role "Designer"

# Add from git history
goal authors import
```

### Listing Authors

```bash
# List all authors
goal authors list
# Output:
# Project Authors:
# ----------------------------------------
#   Alice Chen <alice@company.com> (alice) - Lead Developer
#   Bob Smith <bob@company.com> (bob) - Designer
#   John Doe <john@example.com> [you]
```

### Finding Authors

```bash
# Find by name
goal authors find "Alice"

# Find by email
goal authors find "bob@company.com"

# Find by alias
goal authors find "bob"
```

### Updating Authors

```bash
# Update role
goal authors update alice@company.com --role "Senior Developer"

# Update name
goal authors update bob@company.com --name "Robert Smith"

# Update alias
goal authors update alice@company.com --alias "chen"
```

### Removing Authors

```bash
goal authors remove bob@company.com
```

## Committing with Co-authors

### Single Co-author

```bash
# Stage changes
git add .

# Commit with co-author
goal commit --co-author "Alice Chen <alice@company.com>"

# Generated commit message:
# feat: add user authentication system
#
# Co-authored-by: Alice Chen <alice@company.com>
```

### Multiple Co-authors

```bash
goal commit --co-author "Alice Chen <alice@company.com>" --co-author "Bob Smith <bob@company.com>"

# Generated commit message:
# feat: implement real-time collaboration
#
# Co-authored-by: Alice Chen <alice@company.com>
# Co-authored-by: Bob Smith <bob@company.com>
```

### Using Aliases

If you have aliases set up, you can use them:

```bash
# This would work if "alice" is an alias
goal commit --co-author "alice <alice@company.com>"
```

## Team Workflows

### Feature Branch Collaboration

```bash
# 1. Create feature branch
git checkout -b feature/new-ui

# 2. Work together
git add .
goal commit --co-author "Alice Chen <alice@company.com>" --co-author "Bob Smith <bob@company.com>"

# 3. Push and create PR
git push origin feature/new-ui
```

### Pair Programming Session

```bash
# After pair programming session
git add .
goal commit --co-author "Pair Partner <partner@company.com>"
```

### Code Review Contributions

```bash
# After incorporating review feedback
git add .
goal commit --co-author "Reviewer <reviewer@company.com>"
```

## Exporting Team Information

### Generate CONTRIBUTORS.md

```bash
goal authors export
```

This creates a `CONTRIBUTORS.md` file:

```markdown
# Contributors

This project exists thanks to all the people who contribute:

- **Alice Chen** <alice@company.com> - Lead Developer
- **Bob Smith** <bob@company.com> - Designer
- **John Doe** <john@example.com> - Contributor
```

## Project Configuration

Authors are stored in your project's `goal.yaml`:

```yaml
authors:
  - name: Alice Chen
    email: alice@company.com
    role: Lead Developer
    alias: alice
  - name: Bob Smith
    email: bob@company.com
    role: Designer
    alias: bob
  - name: John Doe
    email: john@example.com
```

## Best Practices

1. **Import existing contributors**:
   ```bash
   goal authors import
   ```

2. **Use meaningful roles**:
   - Lead Developer, Senior Developer, Junior Developer
   - Designer, UX Designer, UI Designer
   - Product Manager, Project Manager
   - DevOps Engineer, QA Engineer

3. **Keep aliases short and unique**:
   ```bash
   goal authors add "Very Long Name" long@example.com --alias "longname"
   ```

4. **Export contributors regularly**:
   ```bash
   goal authors export
   git add CONTRIBUTORS.md
   goal commit -m "docs: update contributors"
   ```

5. **Use co-authors for collaborative work**:
   - Pair programming sessions
   - Code reviews with significant contributions
   - Cross-team collaboration
   - Mentored contributions

## Integration with GitHub

GitHub automatically recognizes co-author trailers:

- Co-authors appear on commit details
- Contribution graphs include co-authors
- PR reviews show collaborative commits

## Example Project Timeline

```bash
# Project setup
goal wizard
goal authors import

# Team joins
goal authors add "Alice" alice@company.com --role "Developer"
goal authors add "Bob" bob@company.com --role "Designer"

# Feature development
git add feature.py
goal commit --co-author "Alice <alice@company.com>"

# Design updates
git add design.css
goal commit --co-author "Bob <bob@company.com>"

# Collaborative feature
git add .
goal commit --co-author "Alice <alice@company.com>" --co-author "Bob <bob@company.com>"

# Release
goal push --all

# Update contributors
goal authors export
git add CONTRIBUTORS.md
goal commit -m "docs: update contributors"
goal push
```
