# Ruby Project Example

Example Ruby gem with Goal integration.

## Usage with Goal

```bash
# Install dependencies
bundle install

# Initialize Goal
goal init

# Run tests
bundle exec rspec

# Full release
goal --all
```

## Configuration

```yaml
version: "1.0"

project:
  name: "goal_example"
  type: "ruby"
  versioning:
    strategy: "semantic"

testing:
  command: "bundle exec rspec"

publishing:
  enabled: true
  registry: "rubygems"
  build_command: "gem build *.gemspec"
  upload_command: "gem push *.gem"
```

## Gem Publishing

```bash
# Build gem
gem build goal_example.gemspec

# Push to RubyGems
gem push goal_example-1.0.0.gem
```
