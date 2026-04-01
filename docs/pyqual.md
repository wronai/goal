# Pyqual Quality Pipeline

Dokumentacja pipeline jakości opartego na **pyqual** z automatycznymi naprawami przez AI.

## Architektura Pipeline

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   setup     │───▶│    test     │───▶│  prefact    │
│(deps check) │    │  (pytest)   │    │(AI refactor)│
└─────────────┘    └─────────────┘    └─────────────┘
                                             │
                        ┌────────────────────┘
                        ▼ (when metrics fail)
               ┌─────────────┐
               │ claude_fix  │
               │(Claude Code)│
               └─────────────┘
                        │
                        ▼
               ┌─────────────┐
               │   verify    │
               │(re-validate)│
               └─────────────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
        ▼ (metrics_pass)                ▼ (metrics_fail)
┌─────────────┐                 ┌─────────────┐
│  push +     │                 │ next iter   │
│  publish    │                 │ (max 3)     │
└─────────────┘                 └─────────────┘
```

## Konfiguracja (`pyqual.yaml`)

```yaml
pipeline:
  name: quality-loop-with-llx

  # Gate'y jakości - wszystkie muszą przejść
  metrics:
    cc_max: 20           # Cyclomatic complexity per function
    critical_max: 20     # Critical issues threshold
    vallm_pass_min: 50   # vallm validation pass rate (%)

  stages:
    # Verify/install all tool dependencies
    - name: setup
      run: |
        set -e
        for pkg in code2llm vallm prefact llx pytest-cov goal; do
          python -m pip show "$pkg" >/dev/null 2>&1 || pip install -q "$pkg"
        done
      when: first_iteration
      timeout: 300

    # Run tests with coverage
    - name: test
      run: python3 -m pytest -q --cov=goal --cov-report=term-missing
      optional: true

    # AI refactoring when metrics fail
    - name: prefact
      tool: prefact
      optional: true
      when: metrics_fail
      timeout: 900

    # Claude Code fix (fallback)
    - name: claude_fix
      run: |
        export PATH="$HOME/.local/bin:$PATH"
        if command -v claude >/dev/null 2>&1 && [ -f TODO.md ] && [ -s TODO.md ]; then
          timeout 900 claude -p "Fix quality issues: $(head -50 TODO.md)" \
            --model sonnet --allowedTools "Edit,Read,Write" \
            --output-format text || echo "Claude fix failed"
        fi
      when: metrics_fail
      timeout: 1200

    # Re-validation after fixes
    - name: verify
      run: vallm batch pyqual tests --recursive --format toon --output ./project
      optional: true
      when: after_fix
      timeout: 300

    # Generate metrics report
    - name: report
      tool: report
      when: metrics_pass
      optional: true

    # Git push when all gates pass
    - name: push
      run: |
        if [ -n "$(git status --porcelain)" ]; then
          git add -A
          git commit -m "chore: pyqual auto-commit [skip ci]" 2>/dev/null || true
          git push origin HEAD
        fi
      when: metrics_pass
      optional: true
      timeout: 120

    # Build package for PyPI
    - name: publish
      run: |
        echo "=== Building package ==="
        make build
        echo "To upload: twine upload dist/* --username __token__"
      when: metrics_pass
      optional: true
      timeout: 300

  # Loop configuration
  loop:
    max_iterations: 3
    on_fail: report

  env:
    LLM_MODEL: openrouter/x-ai/grok-code-fast-1
    LLX_DEFAULT_TIER: balanced
```

## Użycie

### Lokalne uruchomienie

```bash
# Zainstaluj pyqual
pip install pyqual

# Uruchom pipeline
pyqual run --config pyqual.yaml

# Tylko walidacja (bez wykonania)
pyqual validate --config pyqual.yaml

# Status metryk
pyqual status --config pyqual.yaml

# Szczegółowe logi
pyqual run --config pyqual.yaml --verbose
```

### CI/CD (GitHub Actions)

```yaml
# .github/workflows/quality.yml
name: Quality Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -e ".[dev]"
          pip install pyqual tox
      
      - name: Run quality pipeline
        run: pyqual run --config pyqual.yaml
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          PYPI_TOKEN: ${{ secrets.PYPI_TOKEN }}
```

## Stage'y

| Stage | Opis | Warunek uruchomienia | Timeout |
|-------|------|---------------------|---------|
| `setup` | Instalacja zależności | `first_iteration` | 300s |
| `test` | Pytest + coverage | `always` | - |
| `prefact` | AI refactoring | `metrics_fail` | 900s |
| `claude_fix` | Claude Code CLI fix | `metrics_fail` | 1200s |
| `verify` | Re-walidacja po naprawach | `after_fix` | 300s |
| `report` | Generowanie raportu | `metrics_pass` | - |
| `push` | Git push | `metrics_pass` | 120s |
| `publish` | Build PyPI | `metrics_pass` | 300s |
| `markdown_report` | Raport markdown | `always` | 30s |

## Gate'y jakości

Obecne gate'y w projekcie:

- **CC** (Cyclomatic Complexity) ≤ 20 - złożoność cyklomatyczna na funkcję
  - Obecna wartość: 4.8 ✓
  
- **Critical** ≤ 20 - liczba krytycznych problemów
  - Obecna wartość: 17.0 ✓
  
- **Vallm pass** ≥ 50% - procent poprawnych walidacji vallm
  - Obecna wartość: 100% ✓

## Claude Code Integration

### Wymagania

```bash
# Instalacja Claude Code CLI
npm install -g @anthropic-ai/claude-code

# Autentykacja lokalna
claude auth login

# Lub w CI - zmienna środowiskowa
export ANTHROPIC_API_KEY=sk-ant-...
```

### Użycie

Claude Code jest używane automatycznie gdy:
1. Gate'y jakości **nie** przechodzą
2. Stage `prefact` nie rozwiązał problemów
3. Claude CLI jest dostępny w PATH

Prompt zawiera:
- Pierwsze 50 linii z `TODO.md`
- Kontekst projektu (pliki, struktura)

## Troubleshooting

### Coverage nie jest parsowane

```bash
# Problem: pyqual nie wspiera parsowania pytest-cov
# Rozwiązanie: użyj gate na podstawie innych metryk
# lub zapisz coverage do pliku i parsuj ręcznie

pytest --cov=goal --cov-report=xml
# Dodaj stage parsujący coverage.xml
```

### Claude Code nie działa

```bash
# Sprawdź instalację
which claude
claude --version

# Sprawdź autentykację
claude auth status

# W CI użyj ANTHROPIC_API_KEY
```

### Pipeline się zapętla

```yaml
# W pyqual.yaml - zmniejsz iteracje lub wyłącz stage
loop:
  max_iterations: 1  # Zamiast 3

# Lub oznacz stage jako optional
- name: prefact
  optional: true
```

### Push fail (brak uprawnień)

```bash
# Lokalnie - skonfiguruj git
git config user.name "Developer"
git config user.email "dev@example.com"

# W CI - użyj tokena
GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Tox - testowanie wielu wersji Python

Skonfigurowane w `pyproject.toml`:

```toml
[tool.tox]
legacy_tox_ini = """
[tox]
envlist = py38,py39,py310,py311,py312
isolated_build = true

[testenv]
deps =
    pytest>=7.0.0
    build
    twine
    pfix>=0.1.60
extras = nfo
commands = pytest {posargs}

[testenv:lint]
deps = pfix>=0.1.60
commands = pfix check {posargs}

[testenv:pyqual]
deps = pyqual>=0.2.0
commands = pyqual validate --config pyqual.yaml
"""
```

### Uruchomienie

```bash
# Zainstaluj tox
pip install tox

# Testuj wszystkie wersje
tox

# Konkretna wersja
tox -e py311

# Tylko lint
tox -e lint

# Walidacja pyqual
tox -e pyqual
```

## Powiązane narzędzia

- **pyqual** - Pipeline jakości i iteracyjne naprawy
- **prefact** - AI refactoring kodu
- **vallm** - Walidacja kodu przez LLM
- **code2llm** - Analiza kodu dla LLM
- **llx** - Fallback LLM fixes
- **tox** - Testowanie wielu środowisk

## Zobacz też

- [CI/CD Integration](./ci-cd.md) - Pełna dokumentacja CI/CD
- [Testing Guide](./usage.md) - Testowanie w goal
- [Configuration](./configuration.md) - Konfiguracja goal.yaml
