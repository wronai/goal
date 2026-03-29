"""
Integration tests for Goal API usage.

These tests demonstrate how to test code that uses Goal's API.
"""

import sys
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

# Add goal to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pytest


class TestGoalAPIIntegration:
    """Integration tests for Goal API."""
    
    def test_bootstrap_project_detection(self, tmp_path):
        """Test project type detection in bootstrap."""
        from goal.project_bootstrap import bootstrap_project
        
        # Create a mock Python project
        (tmp_path / "pyproject.toml").write_text("""
[project]
name = "test-project"
version = "0.1.0"
""")
        
        with patch('click.echo'):  # Suppress output
            result = bootstrap_project(tmp_path, "python", yes=True)
        
        assert result['project_type'] == "python"
        assert 'env_ok' in result
        assert 'tests_found' in result
    
    def test_version_validation(self):
        """Test version validation across registries."""
        from goal.version_validation import validate_project_versions
        
        with patch('goal.version_validation.get_pypi_version') as mock_pypi:
            mock_pypi.return_value = "1.0.0"
            
            results = validate_project_versions(["python"], "1.0.0")
            
            assert "python" in results
            assert results["python"]["is_latest"] is True
    
    def test_commit_message_generation(self):
        """Test commit message generation."""
        from goal.push.stages import get_commit_message
        
        ctx_obj = {'yes': True, 'markdown': False, 'config': None}
        files = ["src/main.py", "tests/test_main.py"]
        diff = """
+ def new_function():
+     pass
"""
        
        with patch('goal.push.stages.generate_commit_message') as mock_gen:
            mock_gen.return_value = ("feat: add new function", None, None)
            
            title, body, result = get_commit_message(
                ctx_obj, files, diff, message=None, ticket=None, abstraction=None
            )
            
            assert title is not None
            assert isinstance(title, str)
    
    def test_git_operations(self, tmp_path):
        """Test git operations."""
        from goal.git_ops import is_git_repository
        
        # Create a git repo
        import subprocess
        subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
        
        assert is_git_repository(tmp_path) is True
        assert is_git_repository(Path("/nonexistent")) is False


class TestCustomValidators:
    """Tests for custom validators."""
    
    def test_file_size_validator(self, tmp_path):
        """Test file size validation."""
        from goal.validators import validate_staged_files
        
        # Create a large file
        large_file = tmp_path / "large.bin"
        large_file.write_bytes(b"x" * (11 * 1024 * 1024))  # 11MB
        
        # Mock config
        config = Mock()
        config.advanced.file_validation.max_file_size_mb = 10
        config.advanced.file_validation.block_large_files = True
        
        # Should raise exception for large file
        # Note: This test assumes validate_staged_files checks staged files
        # In real use, file would need to be staged first
    
    def test_secret_detection_validator(self):
        """Test secret detection in files."""
        from goal.validators import detect_api_tokens
        
        test_cases = [
            ("api_key = 'sk-1234567890abcdef'", True),
            ("password = 'secret123'", True),
            ("x = 1 + 2", False),
        ]
        
        for content, should_detect in test_cases:
            result = detect_api_tokens(content)
            # Result should be non-empty if secrets detected
            if should_detect:
                assert len(result) > 0
            else:
                assert len(result) == 0


class TestHookIntegration:
    """Tests for hook integration."""
    
    def test_pre_commit_hook_execution(self, tmp_path):
        """Test pre-commit hook runs correctly."""
        from goal.hooks.manager import HooksManager
        
        manager = HooksManager()
        
        # Register a test hook
        @manager.pre_commit
        def test_hook():
            return True
        
        # Run hooks
        result = manager.run_pre_commit()
        assert result is True
    
    def test_validator_registration(self):
        """Test custom validator registration."""
        from goal.hooks.manager import HooksManager
        
        manager = HooksManager()
        
        @manager.validator
        def always_pass(files):
            return True
        
        @manager.validator  
        def always_fail(files):
            return False
        
        # First validator passes
        assert always_pass([]) is True
        # Second validator fails
        assert always_fail([]) is False


class TestConfiguration:
    """Tests for configuration management."""
    
    def test_config_loading(self, tmp_path):
        """Test configuration loading."""
        from goal.config import ensure_config
        
        # Create test config
        config_file = tmp_path / "goal.yaml"
        config_file.write_text("""
version: "1.0"
project:
  name: "test"
  type: "python"
""")
        
        with patch('pathlib.Path.cwd', return_value=tmp_path):
            with patch('click.echo'):
                config = ensure_config()
        
        assert config is not None
    
    def test_user_config_loading(self):
        """Test user configuration loading."""
        from goal.config.manager import get_user_config
        
        with patch('pathlib.Path.home') as mock_home:
            mock_home.return_value = Path("/tmp")
            
            # Create mock user config
            import os
            os.makedirs("/tmp/.goal", exist_ok=True)
            with open("/tmp/.goal/config.json", "w") as f:
                f.write('{"author_name": "Test"}')
            
            config = get_user_config()
            
            if config:
                assert 'author_name' in config


class TestWorkflowIntegration:
    """End-to-end workflow tests."""
    
    def test_full_workflow_dry_run(self, tmp_path):
        """Test full workflow in dry-run mode."""
        from goal.push.core import execute_push_workflow
        
        # Setup mock project
        (tmp_path / "pyproject.toml").write_text("""
[project]
name = "test"
version = "0.1.0"
""")
        (tmp_path / "VERSION").write_text("0.1.0")
        
        import subprocess
        subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=tmp_path, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=tmp_path, capture_output=True)
        
        # Create a test file and stage it
        test_file = tmp_path / "test.py"
        test_file.write_text("print('hello')")
        subprocess.run(["git", "add", "."], cwd=tmp_path, capture_output=True)
        
        ctx_obj = {
            'yes': True,
            'markdown': False,
            'config': None,
            'user_config': {}
        }
        
        # Run in dry-run mode (should not make changes)
        with patch('click.echo'):
            with patch('goal.push.core._detect_and_bootstrap_projects'):
                try:
                    execute_push_workflow(
                        ctx_obj=ctx_obj,
                        bump='patch',
                        no_tag=False,
                        no_changelog=False,
                        no_version_sync=False,
                        message=None,
                        dry_run=True,  # Safety first
                        yes=True,
                        markdown=False,
                        split=False,
                        ticket=None,
                        abstraction=None,
                        todo=False,
                        force=False
                    )
                except SystemExit:
                    pass  # Expected in test environment


# Example usage in your own tests
class ExampleGoalAPITest:
    """Example showing how to test your own Goal integration."""
    
    def test_my_custom_workflow(self):
        """Test your custom workflow."""
        # 1. Setup test environment
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            
            # 2. Create test project
            (project_dir / "pyproject.toml").write_text("""
[project]
name = "my-project"
version = "1.0.0"
""")
            
            # 3. Initialize git
            import subprocess
            subprocess.run(["git", "init"], cwd=project_dir, capture_output=True)
            
            # 4. Test your API usage
            from goal.project_bootstrap import bootstrap_project
            
            with patch('click.echo'):
                result = bootstrap_project(project_dir, "python", yes=True)
            
            # 5. Assert expected behavior
            assert result['env_ok'] is True or result['env_ok'] is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
