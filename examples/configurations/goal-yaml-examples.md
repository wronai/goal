# Example goal.yaml configurations for different scenarios

## Table of Contents

1. [Minimal Configuration](#minimal-configuration)
2. [Python Package](#python-package)
3. [Node.js Application](#nodejs-application)
4. [Monorepo Setup](#monorepo-setup)
5. [Library with Strict Quality Gates](#library-with-strict-quality-gates)
6. [Team Project with Multiple Authors](#team-project-with-multiple-authors)
7. [CI/CD Optimized](#cicd-optimized)
8. [Advanced with Custom Hooks](#advanced-with-custom-hooks)

---

## Minimal Configuration

Basic setup for simple projects.

```yaml
version: "1.0"

project:
  name: "my-project"
  type: "python"
  versioning:
    strategy: "semantic"
    initial_version: "0.1.0"

commit:
  conventional:
    enabled: true
    types: ["feat", "fix", "docs", "chore"]
```

## Python Package

Full-featured Python package configuration.

```yaml
version: "1.0"

project:
  name: "my-package"
  description: "A Python package for doing things"
  type: "python"
  versioning:
    strategy: "semantic"
    files:
      - pyproject.toml
      - src/my_package/__init__.py
  
  author:
    name: "Your Name"
    email: "you@example.com"
  
  license: "MIT"

commit:
  conventional:
    enabled: true
    types: ["feat", "fix", "docs", "style", "refactor", "test", "chore"]
    scopes: ["api", "cli", "core", "tests", "docs"]
    require_scope: false
  
  enhanced_summary:
    enabled: true
    include_test_info: true
    include_file_stats: true

testing:
  command: "pytest tests/ -v --cov=src/my_package"
  coverage_threshold: 80
  fail_under_threshold: true

changelog:
  enabled: true
  file: "CHANGELOG.md"
  format: "keep-a-changelog"
  sections:
    - "Added"
    - "Changed"
    - "Deprecated"
    - "Removed"
    - "Fixed"
    - "Security"

publishing:
  enabled: true
  registry: "pypi"
  build_command: "python -m build"
  upload_command: "twine upload dist/*"
  skip_existing: true

advanced:
  file_validation:
    max_file_size_mb: 10
    block_large_files: true
    detect_api_tokens: true
    auto_manage_gitignore: true
  
  security:
    required_checks:
      - "no_secrets"
      - "tests_pass"
```

## Node.js Application

Configuration for Node.js/TypeScript projects.

```yaml
version: "1.0"

project:
  name: "my-app"
  type: "nodejs"
  versioning:
    strategy: "semantic"
    files:
      - package.json
      - package-lock.json

commit:
  conventional:
    enabled: true
    types: ["feat", "fix", "docs", "style", "refactor", "test", "chore", "perf", "ci"]
  
  enhanced_summary:
    enabled: true
    include_dependencies_changes: true

testing:
  command: "npm test"
  coverage_threshold: 70
  fail_under_threshold: false

changelog:
  enabled: true
  file: "CHANGELOG.md"

publishing:
  enabled: true
  registry: "npm"
  build_command: "npm run build"
  upload_command: "npm publish"
  access: "public"

advanced:
  nodejs:
    package_manager: "npm"  # or "yarn", "pnpm"
    run_build_before_publish: true
    include_dev_dependencies_in_lock: true
```

## Monorepo Setup

Multi-package repository configuration.

```yaml
version: "1.0"

project:
  name: "my-monorepo"
  type: "monorepo"
  versioning:
    strategy: "synchronized"  # or "independent"
    files:
      - VERSION
      - packages/*/package.json
      - packages/*/pyproject.toml

commit:
  conventional:
    enabled: true
    require_scope: true
    scopes: ["frontend", "backend", "shared", "docs", "ci"]
  
  enhanced_summary:
    enabled: true
    include_package_info: true

advanced:
  monorepo:
    packages_dir: "packages"
    release_strategy: "coordinated"  # Release all together
    # or "independent" for separate releases
    
    packages:
      frontend:
        type: "nodejs"
        path: "packages/frontend"
        test_command: "npm test"
        publish: true
        
      backend:
        type: "python"
        path: "packages/backend"
        test_command: "pytest"
        publish: true
        
      shared:
        type: "nodejs"
        path: "packages/shared"
        publish: true
        
    dependencies:
      # Define cross-package dependencies
      frontend: ["shared"]
      backend: []
      shared: []
```

## Library with Strict Quality Gates

For projects requiring high quality standards.

```yaml
version: "1.0"

project:
  name: "high-quality-lib"
  type: "python"
  versioning:
    strategy: "semantic"

commit:
  conventional:
    enabled: true
    require_scope: true
    strict: true
    
  enhanced_summary:
    enabled: true
    quality_gates:
      min_description_length: 50
      require_test_mention: true
      require_issue_reference: true

testing:
  command: "pytest tests/ -v --cov=src --cov-report=term-missing"
  coverage_threshold: 95
  fail_under_threshold: true
  
  additional_checks:
    - "mypy src/ --strict"
    - "flake8 src/ tests/"
    - "black --check src/ tests/"
    - "pylint src/"

quality:
  enabled: true
  
  static_analysis:
    enabled: true
    tools:
      - "mypy"
      - "pylint"
      - "flake8"
      - "bandit"
  
  formatting:
    enabled: true
    tool: "black"
    line_length: 88
  
  complexity:
    max_cyclomatic_complexity: 10
    max_function_length: 50

changelog:
  enabled: true
  require_detailed_entries: true

advanced:
  strict_mode: true
  require_approval_for_breaking_changes: true
  require_two_factor_auth_for_publish: true
```

## Team Project with Multiple Authors

Configuration for team collaboration.

```yaml
version: "1.0"

project:
  name: "team-project"
  type: "python"
  
  authors:
    primary:
      name: "Lead Developer"
      email: "lead@example.com"
      
    contributors:
      - name: "Developer One"
        email: "dev1@example.com"
        role: "Backend"
        
      - name: "Developer Two"
        email: "dev2@example.com"
        role: "Frontend"
        
      - name: "Developer Three"
        email: "dev3@example.com"
        role: "DevOps"

commit:
  conventional:
    enabled: true
    
  co_authors:
    enabled: true
    auto_add_from_git_history: true
    
  attribution:
    require_signoff: true
    require_cla: false

review:
  enabled: true
  require_approval: true
  min_approvers: 1
  require_code_owner_review: true
  
  code_owners:
    "src/core/**": ["@lead-dev"]
    "src/api/**": ["@backend-team"]
    "src/ui/**": ["@frontend-team"]

advanced:
  team:
    auto_assign_reviewers: true
    notify_on_build_failure: true
    
  collaboration:
    enable_pair_programming_mode: false
    track_contributor_stats: true
```

## CI/CD Optimized

Configuration optimized for automated CI/CD pipelines.

```yaml
version: "1.0"

project:
  name: "ci-optimized-project"
  type: "python"

commit:
  conventional:
    enabled: true
    # In CI, we trust the message provided
    auto_generate: false

testing:
  command: "pytest tests/ -v --tb=short"
  coverage_threshold: 80
  fail_under_threshold: true
  parallel: true
  max_workers: 4

changelog:
  enabled: true
  auto_generate: true
  include_pr_links: true

publishing:
  enabled: true
  dry_run_in_ci: false
  
  # CI-specific settings
  ci:
    require_all_checks_pass: true
    require_branch: "main"
    skip_tests_in_ci: false
    auto_rollback_on_failure: true

advanced:
  ci:
    provider: "github-actions"  # or "gitlab-ci", "jenkins", "azure-devops"
    
    github_actions:
      workflow_file: ".github/workflows/release.yml"
      enable_matrix_testing: true
      test_python_versions: ["3.8", "3.9", "3.10", "3.11"]
      
    cache:
      enabled: true
      paths:
        - ".venv"
        - "__pycache__"
        - ".pytest_cache"
    
    notifications:
      on_success: true
      on_failure: true
      channels:
        - "slack"
        - "email"
```

## Advanced with Custom Hooks

Configuration with custom hooks and validators.

```yaml
version: "1.0"

project:
  name: "advanced-project"
  type: "python"

commit:
  conventional:
    enabled: true

advanced:
  hooks:
    pre-commit: ".goal/hooks/pre-commit.py"
    post-commit: ".goal/hooks/post-commit.py"
    pre-push: ".goal/hooks/pre-push.py"
    pre-publish: ".goal/hooks/pre-publish.py"
  
  validators:
    custom:
      - name: "security_scan"
        script: ".goal/validators/security.py"
        fail_on_error: true
        
      - name: "performance_check"
        script: ".goal/validators/performance.py"
        fail_on_error: false  # Just warn
        
      - name: "documentation_check"
        script: ".goal/validators/docs.py"
        fail_on_error: true
  
  plugins:
    enabled:
      - "goal-plugin-slack"
      - "goal-plugin-jira"
    
    slack:
      webhook_url: "${SLACK_WEBHOOK_URL}"
      channel: "#deployments"
      notify_on:
        - "commit"
        - "publish"
        
    jira:
      server: "https://company.atlassian.net"
      project_key: "PROJ"
      auto_transition_on_commit: true

  security:
    secret_detection:
      enabled: true
      patterns:
        - "api_key"
        - "password"
        - "secret"
        - "token"
      
    required_checks:
      - "no_hardcoded_secrets"
      - "no_private_keys"
      - "dependency_vulnerability_scan"
      - "license_compliance"

  performance:
    max_commit_time_seconds: 300
    max_publish_time_seconds: 600
    
    benchmarks:
      enabled: true
      fail_on_regression: true
      max_regression_percent: 10
```

---

## Environment-Specific Overrides

You can also create environment-specific config files:

- `goal.local.yaml` - Local development overrides (gitignored)
- `goal.ci.yaml` - CI/CD specific settings
- `goal.prod.yaml` - Production release settings

Example `goal.local.yaml`:

```yaml
# Override for local development
testing:
  coverage_threshold: 50  # Lower threshold for local
  fail_under_threshold: false

advanced:
  hooks:
    pre-commit: null  # Disable in local dev
```

## Tips

1. **Start simple**: Begin with minimal config and add as needed
2. **Use environment variables**: For secrets and environment-specific values
3. **Document custom hooks**: Add comments explaining what each hook does
4. **Test config changes**: Use `--dry-run` to test configuration changes
5. **Version your config**: Track goal.yaml changes in git

## Validation

Validate your configuration:

```bash
goal config validate
```

Check for updates:

```bash
goal config update
```
