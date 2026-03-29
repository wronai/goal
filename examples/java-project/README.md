# Java Project Example

Example Java/Maven project with Goal integration.

## Usage with Goal

```bash
# Initialize Goal
goal init

# Run tests
mvn test

# Full release
goal --all
```

## Configuration

```yaml
version: "1.0"

project:
  name: "goal-java-example"
  type: "java"
  versioning:
    strategy: "semantic"
    files:
      - pom.xml

testing:
  command: "mvn test"

publishing:
  enabled: true
  registry: "maven-central"
  build_command: "mvn clean package"
  upload_command: "mvn deploy"
```

## Maven Publishing

Requires `~/.m2/settings.xml` with credentials:

```xml
<settings>
  <servers>
    <server>
      <id>ossrh</id>
      <username>YOUR_USERNAME</username>
      <password>YOUR_PASSWORD</password>
    </server>
  </servers>
</settings>
```
