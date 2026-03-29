# Go Project Example

Example Go project with Goal integration.

## Structure

```
go-project/
├── main.go           # Main application
├── go.mod            # Go module definition
└── README.md         # This file
```

## Usage with Goal

```bash
# Initialize Goal
goal init

# Run tests (default: go test ./...)
go test ./...

# Full release
goal --all

# Or step by step
goal push --yes --bump minor
```

## Configuration

Create `goal.yaml`:

```yaml
version: "1.0"

project:
  name: "myapp"
  type: "go"
  versioning:
    strategy: "semantic"

commit:
  conventional:
    enabled: true

testing:
  command: "go test ./... -v"

publishing:
  enabled: false  # Go uses git tags for publishing
```

## Notes

- Go projects typically don't publish to a registry
- Version is managed through git tags
- Goal creates tags like `v1.0.0`
