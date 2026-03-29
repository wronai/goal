# PHP Project Example

Example PHP project with Goal integration.

## Usage with Goal

```bash
# Install dependencies
composer install

# Initialize Goal
goal init

# Run tests
composer test

# Full release
goal --all
```

## Configuration

```yaml
version: "1.0"

project:
  name: "php-example"
  type: "php"

testing:
  command: "composer test"

publishing:
  enabled: false  # PHP typically uses Packagist
```

## Packagist Publishing

For Packagist publishing, add to `composer.json`:

```json
{
  "name": "vendor/package",
  "version": "1.0.0",
  "repositories": [
    {
      "type": "vcs",
      "url": "https://github.com/vendor/package"
    }
  ]
}
```
