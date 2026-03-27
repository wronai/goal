# Goal Wizard Setup Example

This example demonstrates how to use the `goal wizard` command to set up a new project from scratch.

## Quick Start

```bash
# Clone this example
git clone https://github.com/wronai/goal.git
cd goal/examples/wizard-setup

# Run the wizard
python3 -m goal wizard
```

## What the Wizard Does

The wizard guides you through:

1. **Git Repository Setup**
   - Initializes git repository if needed
   - Configures remote repository
   - Validates git configuration

2. **User Configuration**
   - Sets author name and email
   - Chooses default license
   - Stores preferences in `~/.goal`

3. **Project Configuration**
   - Sets project name and description
   - Chooses versioning strategy (semantic, calendar, date)
   - Configures commit message strategy
   - Enables automatic changelog updates

4. **Setup Summary**
   - Shows all configured settings
   - Provides next steps

## Example Wizard Session

```
🧙‍♂️  Welcome to the Goal Setup Wizard!
======================================================================

This wizard will guide you through setting up:
  • Git repository configuration
  • User preferences (name, email, license)
  • Project-specific settings
  • Build and deployment strategies

Continue with setup? [Y/n]: Y

📁 Step 1: Git Repository Setup
----------------------------------------
✓ Already in a git repository: /path/to/project
✓ Git remotes configured:
  origin  git@github.com:user/repo.git (fetch)
  origin  git@github.com:user/repo.git (push)

👤 Step 2: User Configuration
----------------------------------------
✓ User configuration already exists:
  Name: John Doe
  Email: john@example.com
  License: MIT

⚙️  Step 3: Project Configuration
----------------------------------------
✓ Found existing goal.yaml
Detected project information:
  Name: my-project
  Type: python
  Description: A Python project
  Version: 1.0.0

Customize project settings? [y/N]: Y

Project name [my-project]: my-awesome-project
Project description []: An awesome Python project

Versioning strategy:
  1. Semantic Versioning (1.2.3)
  2. Calendar Versioning (2024.03.15)
  3. Date Versioning (20240315)
Choose strategy [1]: 1

Commit message strategy:
  1. Conventional Commits (feat, fix, docs, etc.)
  2. Semantic Commits (with scope)
  3. Custom format
Choose strategy [1]: 1

Automatically update CHANGELOG.md? [Y/n]: Y

✓ Project configuration saved to goal.yaml

📝 Setup Summary
========================================
User Configuration:
  Author: John Doe <john@example.com>
  License: MIT License

Project Configuration:
  Name: my-awesome-project
  Description: An awesome Python project
  Versioning: semver
  Commits: conventional

Git Repository:
  Root: /path/to/project
  Status: Clean

✨ Setup complete! You're ready to use Goal.

Next steps:
  1. Make some changes to your code
  2. Run: goal commit
  3. Review and confirm the generated commit message
```

## Generated Configuration

After running the wizard, you'll have:

### `~/.goal` (User Config)
```yaml
author_name: John Doe
author_email: john@example.com
license: MIT
license_name: MIT License
license_classifier: MIT License
```

### `goal.yaml` (Project Config)
```yaml
project:
  name: my-awesome-project
  description: An awesome Python project
  type: [python]
  version: 1.0.0

versioning:
  strategy: semver

git:
  commit:
    strategy: conventional

changelog:
  auto_update: true
```

## Next Steps

1. Make some changes to your code
2. Stage the changes: `git add .`
3. Generate a commit message: `goal commit`
4. Complete the workflow: `goal push`

## Tips

- Run `goal wizard --reset` to reconfigure everything
- Use `goal wizard --skip-git` to skip git setup
- Use `goal wizard --skip-user` to skip user configuration
- Use `goal wizard --skip-project` to skip project configuration
