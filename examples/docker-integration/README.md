# Docker Integration for Goal

Examples of using Goal with Docker containers.

## Quick Start

### Dockerfile

```dockerfile
# Build stage
FROM python:3.11-slim as builder

WORKDIR /app
COPY pyproject.toml ./
RUN pip install --no-cache-dir build

COPY . .
RUN python -m build

# Runtime stage
FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /app/dist/*.whl ./
RUN pip install --no-cache-dir *.whl

CMD ["python", "-m", "myapp"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build: .
    volumes:
      - .:/app
    environment:
      - GOAL_CI=true
  
  test:
    build: .
    command: pytest
    volumes:
      - .:/app
```

## Usage

### Build and Test

```bash
# Build image
docker build -t myapp .

# Run tests in container
docker run myapp pytest

# Release with Goal in container
docker run -v $(pwd):/app -w /app myapp goal --all
```

### Docker-in-Docker Release

```bash
# Release with Docker socket
docker run -v /var/run/docker.sock:/var/run/docker.sock \
  -v $(pwd):/app \
  -w /app \
  goal-image \
  goal --all
```

## CI/CD with Docker

### GitHub Actions

```yaml
name: Docker Release

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build image
        run: docker build -t myapp .
      
      - name: Test in container
        run: docker run myapp pytest
      
      - name: Release
        run: |
          docker run \
            -v ${{ github.workspace }}:/app \
            -w /app \
            -e PYPI_TOKEN=${{ secrets.PYPI_TOKEN }} \
            goal-image \
            goal --all --yes
```

## Goal Configuration for Docker

```yaml
version: "1.0"

project:
  name: "dockerized-app"
  type: "python"

advanced:
  docker:
    enabled: true
    image_name: "myapp"
    registry: "docker.io"
    
    build:
      context: "."
      dockerfile: "Dockerfile"
      platforms: ["linux/amd64", "linux/arm64"]
    
    push:
      enabled: true
      tags:
        - "latest"
        - "{version}"
    
    test:
      enabled: true
      command: "docker run myapp pytest"
```

## Multi-Stage Release

```bash
# 1. Build and test in container
docker build --target test -t myapp:test .
docker run myapp:test

# 2. Build release image
docker build -t myapp:latest .

# 3. Run Goal release
goal --all

# 4. Tag and push Docker image
docker tag myapp:latest myapp:v$(cat VERSION)
docker push myapp:v$(cat VERSION)
```

## Tips

- Use multi-stage builds for smaller images
- Mount `.git` for Goal to detect versions
- Pass tokens via environment variables
- Use `.dockerignore` to exclude unnecessary files
