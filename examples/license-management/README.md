# License Management Example

This example demonstrates how to use the `goal license` command to manage project licenses.

## Quick Start

```bash
# Clone this example
git clone https://github.com/wronai/goal.git
cd goal/examples/license-management

# List available licenses
python3 -m goal license list

# Create a LICENSE file
python3 -m goal license create MIT --fullname "Your Name"
```

## Available Licenses

Goal supports these common licenses out of the box:

- **MIT** - Permissive license
- **Apache-2.0** - Permissive with patent grant
- **GPL-3.0** - Strong copyleft
- **BSD-3-Clause** - Permissive 3-clause BSD
- **ISC** - Simple permissive license
- **LGPL-3.0** - Weak copyleft
- **AGPL-3.0** - Strong copyleft with network requirement
- **BSD-2-Clause** - Permissive 2-clause BSD

## Examples

### Creating a LICENSE File

```bash
# Create MIT license
goal license create MIT --fullname "John Doe"

# Create Apache license with specific year
goal license create Apache-2.0 --fullname "John Doe" --year 2024

# Force overwrite existing license
goal license create GPL-3.0 --fullname "John Doe" --force
```

### Checking License Information

```bash
# Get info about a license
goal license info MIT
# Output:
# License: MIT License
# ID: MIT
# Category: permissive
# Type: Permissive

# Check compatibility between licenses
goal license check MIT Apache-2.0
# Output:
# ✓ Compatible
#   MIT is compatible with Apache-2.0

goal license check GPL-3.0 MIT
# Output:
# ✗ Not Compatible
#   Copyleft license GPL-3.0 may not be compatible with permissive license MIT
```

### Updating an Existing License

```bash
# Update copyright year
goal license update --year 2025

# Update copyright holder
goal license update --fullname "Jane Smith"

# Change license type
goal license update --license Apache-2.0
```

### Validating License File

```bash
goal license validate
# Output:
# ✓ LICENSE file is valid

# Or with issues:
# ✗ LICENSE file has issues:
#   • No copyright notice found
#   • License contains unfilled placeholders
```

### Custom License Templates

```bash
# Show a template
goal license template MIT

# Add custom template
goal license template CUSTOM --file my-license.txt

# List custom templates
goal license list --custom
```

## Custom License Template

Create a custom license template:

1. Create a template file `my-license.txt`:
```
My Custom License
Copyright (c) {year} {fullname}

Permission is hereby granted to use, copy, modify, and distribute this software
for any purpose, with or without fee, provided that the above copyright notice
and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
```

2. Add it to Goal:
```bash
goal license template CUSTOM --file my-license.txt
```

3. Use it:
```bash
goal license create CUSTOM --fullname "John Doe"
```

## License Compatibility

Goal provides basic license compatibility checking:

| License | Compatible With |
|---------|-----------------|
| MIT | Apache-2.0, BSD-3-Clause, BSD-2-Clause, ISC, 0BSD |
| Apache-2.0 | MIT, BSD-3-Clause, BSD-2-Clause, ISC, 0BSD |
| GPL-3.0 | GPL-3.0, GPL-2.0, LGPL-3.0, LGPL-2.1 |
| LGPL-3.0 | GPL-3.0, GPL-2.0, LGPL-3.0, LGPL-2.1 |

## Integration with Project Files

When you create or update a license, Goal automatically:

1. Creates/updates the `LICENSE` file
2. Updates license information in:
   - `package.json` (Node.js)
   - `pyproject.toml` (Python)
   - `Cargo.toml` (Rust)
   - `composer.json` (PHP)
   - And other project files

## Best Practices

1. **Choose the right license**:
   - Use MIT for maximum permissiveness
   - Use Apache-2.0 for patent protection
   - Use GPL-3.0 for strong copyleft
   - Use LGPL-3.0 for libraries

2. **Keep copyright updated**:
   ```bash
   # Update yearly
   goal license update --year 2025
   ```

3. **Validate your license**:
   ```bash
   goal license validate
   ```

4. **Check compatibility**:
   ```bash
   # Before using third-party code
   goal license check MIT Apache-2.0
   ```
