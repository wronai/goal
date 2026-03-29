# Template Generator

Quick project scaffolding tool for Goal.

## Usage

```bash
# Generate Python package
python generate.py python my-package --description "My awesome package"

# Generate Node.js app
python generate.py nodejs my-app --author "John Doe"

# Generate Rust crate
python generate.py rust my-crate --license "Apache-2.0"

# Generate Go module
python generate.py go my-module
```

## Available Templates

- `python` - Python package with pyproject.toml
- `nodejs` - Node.js application with npm
- `rust` - Rust crate with Cargo
- `go` - Go module

## Generated Structure

### Python Package

```
my-package/
├── pyproject.toml
├── goal.yaml
├── README.md
├── src/
│   └── my_package/
│       └── __init__.py
└── tests/
    └── test_my_package.py
```

### Node.js App

```
my-app/
├── package.json
├── goal.yaml
├── index.js
└── index.test.js
```

### Rust Crate

```
my-crate/
├── Cargo.toml
├── goal.yaml
└── src/
    ├── lib.rs
    └── main.rs
```

### Go Module

```
my-module/
├── go.mod
├── goal.yaml
├── main.go
└── my-module_test.go
```

## Integration with Goal

After generating:

```bash
cd my-project
goal init     # Initialize Goal
goal --all    # Full release workflow
```

## Extending

Add new templates by editing `TEMPLATES` dict in `generate.py`:

```python
TEMPLATES["my-lang"] = {
    "name": "My Language",
    "files": {
        "config.toml": "...",
        "main.my": "..."
    }
}
```
