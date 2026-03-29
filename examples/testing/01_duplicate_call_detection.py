"""
Test wykrywania duplikowanych wywołań funkcji.

Ten przykład pokazuje jak testować czy funkcje bootstrap
nie są wywoływane wielokrotnie (bug fix dla _ensure_costs_installed).
"""

import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, call
import subprocess

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def test_no_duplicate_costs_install():
    """
    Testuje czy _ensure_costs_installed nie jest wywoływane wielokrotnie.
    
    Bug: Wcześniej funkcja była wywoływana 2x - raz w ensure_project_environment
    i drugi raz w bootstrap_project.
    """
    from goal.project_bootstrap import bootstrap_project, _ensure_costs_installed
    
    with tempfile.TemporaryDirectory() as tmpdir:
        project_dir = Path(tmpdir)
        
        # Tworzymy minimalny projekt Python
        (project_dir / "pyproject.toml").write_text("""
[project]
name = "test-project"
version = "0.1.0"
""")
        
        # Inicjalizujemy git
        subprocess.run(["git", "init"], cwd=project_dir, capture_output=True)
        
        # Mockujemy _ensure_costs_installed aby policzyć wywołania
        call_count = 0
        original_func = _ensure_costs_installed
        
        def counting_mock(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            return True
        
        with patch('goal.project_bootstrap._ensure_costs_installed', side_effect=counting_mock):
            with patch('click.echo'):  # Wyciszamy output
                with patch('goal.project_bootstrap.ensure_project_environment', return_value=True):
                    result = bootstrap_project(project_dir, "python", yes=True)
        
        # Sprawdzamy czy funkcja była wywołana DOKŁADNIE raz
        print(f"_ensure_costs_installed wywołana {call_count} raz(y)")
        
        if call_count == 1:
            print("✓ PASS: Funkcja wywołana dokładnie raz (brak duplikatów)")
        elif call_count == 0:
            print("⚠ WARNING: Funkcja nie została wywołana wcale")
        else:
            print(f"✗ FAIL: Funkcja wywołana {call_count} razy (powinna być 1x)")
        
        return call_count == 1


def test_bootstrap_idempotency():
    """
    Testuje czy bootstrap_project jest idempotentny.
    
    Po wielokrotnym wywołaniu nie powinno być dodatkowych efektów.
    """
    from goal.project_bootstrap import bootstrap_project
    
    with tempfile.TemporaryDirectory() as tmpdir:
        project_dir = Path(tmpdir)
        
        (project_dir / "pyproject.toml").write_text("""
[project]
name = "idempotent-test"
version = "0.1.0"
""")
        
        subprocess.run(["git", "init"], cwd=project_dir, capture_output=True)
        
        # Pierwsze wywołanie
        with patch('click.echo'):
            with patch('goal.project_bootstrap._ensure_costs_installed', return_value=True):
                with patch('goal.project_bootstrap.ensure_project_environment', return_value=True):
                    result1 = bootstrap_project(project_dir, "python", yes=True)
        
        # Drugie wywołanie
        with patch('click.echo'):
            with patch('goal.project_bootstrap._ensure_costs_installed', return_value=True):
                with patch('goal.project_bootstrap.ensure_project_environment', return_value=True):
                    result2 = bootstrap_project(project_dir, "python", yes=True)
        
        # Wyniki powinny być spójne
        print(f"Pierwsze wywołanie: env_ok={result1['env_ok']}")
        print(f"Drugie wywołanie: env_ok={result2['env_ok']}")
        
        if result1['env_ok'] == result2['env_ok']:
            print("✓ PASS: Bootstrap jest idempotentny")
        else:
            print("✗ FAIL: Wyniki różnią się między wywołaniami")


def test_function_call_logging():
    """
    Przykład logowania wywołań funkcji dla debugowania.
    """
    from goal.project_bootstrap import bootstrap_project
    import logging
    
    # Konfiguracja loggera
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("goal.bootstrap")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        project_dir = Path(tmpdir)
        (project_dir / "pyproject.toml").write_text("[project]\nname=\"log-test\"\n")
        subprocess.run(["git", "init"], cwd=project_dir, capture_output=True)
        
        call_log = []
        
        def logged_ensure_costs(project_dir, python_bin):
            call_log.append({
                'function': '_ensure_costs_installed',
                'project_dir': str(project_dir),
                'timestamp': __import__('time').time()
            })
            logger.debug(f"_ensure_costs_installed called for {project_dir}")
            return True
        
        def logged_ensure_env(project_dir, ptype, yes=False):
            call_log.append({
                'function': 'ensure_project_environment',
                'project_dir': str(project_dir),
                'type': ptype
            })
            logger.debug(f"ensure_project_environment called for {ptype}")
            return True
        
        with patch('click.echo'):
            with patch('goal.project_bootstrap._ensure_costs_installed', side_effect=logged_ensure_costs):
                with patch('goal.project_bootstrap.ensure_project_environment', side_effect=logged_ensure_env):
                    bootstrap_project(project_dir, "python", yes=True)
        
        print(f"\nZalogowane wywołania ({len(call_log)}):")
        for i, call_info in enumerate(call_log, 1):
            print(f"  {i}. {call_info['function']}")
        
        # Sprawdź duplikaty
        func_names = [c['function'] for c in call_log]
        duplicates = {name: func_names.count(name) for name in set(func_names) if func_names.count(name) > 1}
        
        if duplicates:
            print(f"\n⚠ Znaleziono duplikaty: {duplicates}")
        else:
            print("\n✓ Brak duplikatów wywołań")


if __name__ == "__main__":
    print("=" * 60)
    print("Testy wykrywania duplikowanych wywołań")
    print("=" * 60)
    
    print("\n1. Test braku duplikatów _ensure_costs_installed:")
    test_no_duplicate_costs_install()
    
    print("\n2. Test idempotentności bootstrap:")
    test_bootstrap_idempotency()
    
    print("\n3. Test logowania wywołań:")
    test_function_call_logging()
    
    print("\n" + "=" * 60)
    print("Testy zakończone")
    print("=" * 60)
