# .NET Project Example

Example .NET project with Goal integration.

## Prerequisites

- .NET SDK 8.0 or later
- Goal installed: `pip install goal`

## Usage with Goal

```bash
# Initialize Goal
goal init

# Run tests
dotnet test

# Build
dotnet build

# Full release
goal --all
```

## Configuration

```yaml
version: "1.0"

project:
  name: "GoalExample"
  type: "dotnet"
  versioning:
    strategy: "semantic"
    files:
      - GoalExample.csproj

testing:
  command: "dotnet test"

publishing:
  enabled: true
  registry: "nuget"
  build_command: "dotnet pack"
  upload_command: "dotnet nuget push *.nupkg"
```

## NuGet Publishing

```bash
# Create NuGet package
dotnet pack

# Push to NuGet (requires API key)
dotnet nuget push bin/Release/*.nupkg --api-key $NUGET_API_KEY --source https://api.nuget.org/v3/index.json
```

## Project Structure

```
dotnet-project/
├── GoalExample.csproj    # Project file
├── Calculator.cs         # Main code
├── CalculatorTests.cs    # Tests
└── goal.yaml            # Goal configuration
```

## Multi-Target Frameworks

For supporting multiple .NET versions:

```xml
<TargetFrameworks>net6.0;net7.0;net8.0</TargetFrameworks>
```
