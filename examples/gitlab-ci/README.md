# GitLab CI Integration for Goal

Examples of using Goal with GitLab CI/CD.

## Basic Configuration

### .gitlab-ci.yml

```yaml
stages:
  - test
  - release

variables:
  GIT_DEPTH: 0  # Needed for Goal to access full history
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

cache:
  paths:
    - .cache/pip
    - .venv/

# Test stage
test:
  stage: test
  image: python:3.11
  before_script:
    - pip install goal pytest
    - goal doctor --fix
  script:
    - pytest tests/ -v
  only:
    - merge_requests
    - main

# Release stage
release:
  stage: release
  image: python:3.11
  before_script:
    - pip install goal
  script:
    - goal --all --yes
  only:
    - main
  variables:
    GIT_COMMITTER_NAME: "GitLab CI"
    GIT_COMMITTER_EMAIL: "ci@example.com"
```

## Advanced Configuration

### With PyPI Publishing

```yaml
release:
  stage: release
  image: python:3.11
  before_script:
    - pip install goal
    - |
      cat > ~/.pypirc << EOF
      [pypi]
      username = __token__
      password = ${PYPI_TOKEN}
      EOF
  script:
    - goal --all --yes
  only:
    - main
  environment:
    name: production
    url: https://pypi.org/project/${CI_PROJECT_NAME}
```

### With Semantic Versioning

```yaml
.release_template: &release
  image: python:3.11
  before_script:
    - pip install goal
    - git config user.email "ci@example.com"
    - git config user.name "GitLab CI"
  script:
    - goal --all --yes --bump ${BUMP_TYPE}

patch_release:
  <<: *release
  variables:
    BUMP_TYPE: patch
  when: manual
  only:
    - main

minor_release:
  <<: *release
  variables:
    BUMP_TYPE: minor
  when: manual
  only:
    - main

major_release:
  <<: *release
  variables:
    BUMP_TYPE: major
  when: manual
  only:
    - main
```

### With Matrix Testing

```yaml
test:
  stage: test
  parallel:
    matrix:
      - PYTHON_VERSION: ["3.8", "3.9", "3.10", "3.11"]
  image: python:${PYTHON_VERSION}
  script:
    - pip install goal pytest
    - pytest tests/ -v
```

## GitLab CI Templates

### Reusable Template

Create `.gitlab/ci/goal.yml`:

```yaml
.goal_release:
  image: python:3.11
  variables:
    GIT_DEPTH: 0
  before_script:
    - pip install goal
    - git config --global user.email "ci@example.com"
    - git config --global user.name "GitLab CI"
  script:
    - goal --all --yes
```

Use in `.gitlab-ci.yml`:

```yaml
include:
  - local: '.gitlab/ci/goal.yml'

release:
  extends: .goal_release
  only:
    - main
```

## Integration with GitLab Features

### Merge Request Comments

```yaml
comment_mr:
  stage: test
  image: python:3.11
  script:
    - |
      curl -X POST \
        -H "PRIVATE-TOKEN: ${GITLAB_TOKEN}" \
        -d "body=Goal release completed: v$(cat VERSION)" \
        "${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/merge_requests/${CI_MERGE_REQUEST_IID}/notes"
  when: on_success
  only:
    - merge_requests
```

### Container Registry

```yaml
build_image:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t ${CI_REGISTRY_IMAGE}:latest .
    - docker push ${CI_REGISTRY_IMAGE}:latest
```

## Environment-Specific Configs

```yaml
# Development
release:dev:
  extends: .goal_release
  variables:
    GOAL_CONFIG: goal.dev.yaml
  environment:
    name: development
  only:
    - develop

# Staging
release:staging:
  extends: .goal_release
  variables:
    GOAL_CONFIG: goal.staging.yaml
  environment:
    name: staging
  only:
    - staging

# Production
release:prod:
  extends: .goal_release
  variables:
    GOAL_CONFIG: goal.prod.yaml
  environment:
    name: production
  when: manual
  only:
    - main
```

## Troubleshooting

### Git History Issues

```yaml
variables:
  GIT_DEPTH: 0  # Full clone needed for Goal
  GIT_STRATEGY: clone
```

### Permission Issues

```yaml
before_script:
  - git config --global user.email "ci@example.com"
  - git config --global user.name "GitLab CI"
  - git remote set-url origin https://ci-token:${CI_JOB_TOKEN}@gitlab.com/${CI_PROJECT_PATH}.git
```

## See Also

- [GitHub Actions](../github-actions/)
- [CI/CD Best Practices](../../docs/ci-cd.md)
