"""
Testowanie wykrywania typów projektów.

Przykłady testów dla funkcji detect_project_types_deep i powiązanych.
"""

import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def test_project_type_detection():
    """Test wykrywania różnych typów projektów."""
    from goal.project_bootstrap import detect_project_types_deep
    
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        
        # Tworzymy strukturę z wieloma typami projektów
        # Python (root)
        (root / "pyproject.toml").write_text("[project]\nname=\"root-py\"\n")
        
        # Node.js (subfolder)
        (root / "frontend").mkdir()
        (root / "frontend" / "package.json").write_text('{"name": "frontend"}')
        
        # Rust (subfolder)
        (root / "backend").mkdir()
        (root / "backend" / "Cargo.toml").write_text("[package]\nname=\"backend\"\n")
        
        # Go (subfolder)
        (root / "cli").mkdir()
        (root / "cli" / "go.mod").write_text("module cli\n")
        
        # Uruchomienie detekcji
        detected = detect_project_types_deep(root, max_depth=1)
        
        print("Wykryte typy projektów:")
        for ptype, dirs in detected.items():
            print(f"  {ptype}: {len(dirs)} lokalizacji")
            for d in dirs:
                print(f"    - {d.name}")
        
        # Weryfikacja
        expected_types = ['python', 'nodejs', 'rust', 'go']
        for expected in expected_types:
            if expected in detected:
                print(f"  ✓ {expected} wykryty")
            else:
                print(f"  ✗ {expected} NIE wykryty")
        
        return detected


def test_nested_project_detection():
    """Test wykrywania zagnieżdżonych projektów."""
    from goal.project_bootstrap import detect_project_types_deep
    
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        
        # Zagnieżdżony projekt Python (2 poziomy)
        (root / "services" / "api").mkdir(parents=True)
        (root / "services" / "api" / "pyproject.toml").write_text("[project]\nname=\"api\"\n")
        
        # max_depth=1 nie powinien wykryć 2 poziomu
        detected_depth1 = detect_project_types_deep(root, max_depth=1)
        print(f"\nZ max_depth=1: {list(detected_depth1.keys())}")
        
        # max_depth=2 powinien wykryć
        detected_depth2 = detect_project_types_deep(root, max_depth=2)
        print(f"Z max_depth=2: {list(detected_depth2.keys())}")
        
        if 'python' not in detected_depth1 and 'python' in detected_depth2:
            print("✓ Zagnieżdżone projekty wykrywane poprawnie wg głębokości")
        else:
            print("ℹ Sprawdź czy max_depth działa jak oczekiwano")


def test_bootstrap_all_projects():
    """Test bootstrap_all_projects z wieloma projektami."""
    from goal.project_bootstrap import bootstrap_all_projects
    import subprocess
    
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        
        # Projekt 1: Python
        (root / "pyproject.toml").write_text("[project]\nname=\"main\"\n")
        subprocess.run(["git", "init"], cwd=root, capture_output=True)
        
        # Projekt 2: Node.js w subfolderze
        (root / "web").mkdir()
        (root / "web" / "package.json").write_text('{"name": "web"}')
        
        # Uruchom bootstrap dla wszystkich
        with patch('click.echo'):
            results = bootstrap_all_projects(root, yes=True)
        
        print(f"\nPrzetworzono {len(results)} projektów:")
        for r in results:
            print(f"  - {r['project_type']} w {r['project_dir'].name}: env_ok={r['env_ok']}")
        
        return results


def test_edge_cases():
    """Test przypadków brzegowych."""
    from goal.project_bootstrap import detect_project_types_deep, PROJECT_BOOTSTRAP
    
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        
        # Pusty katalog
        detected = detect_project_types_deep(root)
        print(f"Pusty katalog: {detected}")
        assert detected == {}, "Pusty katalog powinien zwrócić pusty dict"
        
        # Ukryte katalogi (powinny być ignorowane)
        (root / ".hidden").mkdir()
        (root / ".hidden" / "pyproject.toml").write_text("[project]\n")
        
        detected = detect_project_types_deep(root, max_depth=1)
        print(f"Z ukrytym katalogiem: {detected}")
        # Ukryte katalogi zaczynające się od . powinny być ignorowane
        
        # Nieprawidłowe uprawnienia (symulacja)
        print("\n✓ Testy przypadków brzegowych zakończone")


if __name__ == "__main__":
    print("=" * 60)
    print("Testy wykrywania typów projektów")
    print("=" * 60)
    
    print("\n1. Test wykrywania projektów:")
    test_project_type_detection()
    
    print("\n2. Test zagnieżdżonych projektów:")
    test_nested_project_detection()
    
    print("\n3. Test bootstrap_all_projects:")
    test_bootstrap_all_projects()
    
    print("\n4. Test przypadków brzegowych:")
    test_edge_cases()
    
    print("\n" + "=" * 60)
