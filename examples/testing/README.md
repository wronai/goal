# Testy dla Goal - README

Ten katalog zawiera przykłady testów dla różnych scenariuszy użycia Goal.

## Pliki

### 01_duplicate_call_detection.py
Testy wykrywania duplikowanych wywołań funkcji.

- `test_no_duplicate_costs_install()` - weryfikuje czy `_ensure_costs_installed` nie jest wywoływane wielokrotnie
- `test_bootstrap_idempotency()` - sprawdza idempotentność bootstrap
- `test_function_call_logging()` - logowanie wywołań dla debugowania

**Użycie:**
```bash
python examples/testing/01_duplicate_call_detection.py
```

### 02_project_detection_tests.py
Testy wykrywania typów projektów.

- `test_project_type_detection()` - wykrywanie Python, Node.js, Rust, Go
- `test_nested_project_detection()` - projekty zagnieżdżone na różnych głębokościach
- `test_bootstrap_all_projects()` - bootstrap wielu projektów naraz
- `test_edge_cases()` - przypadki brzegowe

### 03_advanced_mocking.py
Zaawansowane techniki mockowania.

- Mockowanie zewnętrznych usług (PyPI, npm, cargo)
- Mockowanie operacji git
- Mockowanie interakcji click (prompt/confirm)
- Szpiegowanie funkcji i liczenie wywołań
- Mockowanie filesystemu

### 04_debugging_diagnostics.py
Narzędzia diagnostyczne.

- Przechwytywanie outputu debug
- Analiza stack trace
- Pomiar wydajności
- Śledzenie importów
- Generowanie raportów diagnostycznych

## Uruchamianie wszystkich testów

```bash
cd /home/tom/github/wronai/goal

# Pojedynczy plik
python examples/testing/01_duplicate_call_detection.py

# Wszystkie testy
for f in examples/testing/*.py; do
    echo "=== Running: $f ==="
    python "$f"
    echo ""
done
```

## Dodawanie nowych testów

Szablon nowego testu:

```python
def test_my_feature():
    '''Opis testu.'''
    from goal.some_module import some_function
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Setup
        project_dir = Path(tmpdir)
        (project_dir / "pyproject.toml").write_text("...")
        
        # Execute
        with patch('click.echo'):
            result = some_function(project_dir)
        
        # Assert
        assert result is True
        print("✓ Test passed")
```

## Wskazówki

1. **Zawsze używaj `patch('click.echo')`** - wycisza output podczas testów
2. **Używaj `tempfile.TemporaryDirectory()`** - izoluje testy
3. **Mockuj zewnętrzne zależności** - testy są szybsze i bardziej niezawodne
4. **Sprawdzaj duplikaty wywołań** - użyj `call_count` lub `call_history`
