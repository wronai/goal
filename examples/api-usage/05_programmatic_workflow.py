"""
Complete programmatic workflow example.

Shows how to execute a full Goal workflow programmatically.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from goal.push.core import execute_push_workflow


def run_custom_workflow():
    """Run a custom push workflow."""
    print("=" * 60)
    print("Goal API - Programmatic Workflow")
    print("=" * 60)
    
    # Create context object with settings
    ctx_obj = {
        'yes': True,  # Non-interactive mode
        'markdown': False,
        'config': None,
        'user_config': {
            'author_name': 'Developer',
            'author_email': 'dev@example.com'
        },
        'verbose': True
    }
    
    print("\n1. Configuration:")
    print(f"   Auto mode: {ctx_obj['yes']}")
    print(f"   Author: {ctx_obj['user_config']['author_name']}")
    
    print("\n2. Executing workflow...")
    print("   (This would run the full push workflow)")
    print("   - Stage changes")
    print("   - Run tests")
    print("   - Generate commit")
    print("   - Update versions")
    print("   - Push to remote")
    
    # NOTE: This would actually execute the workflow
    # Commented out for safety in example
    
    # execute_push_workflow(
    #     ctx_obj=ctx_obj,
    #     bump='patch',
    #     no_tag=False,
    #     no_changelog=False,
    #     no_version_sync=False,
    #     message=None,
    #     dry_run=True,  # Safety first!
    #     yes=True,
    #     markdown=False,
    #     split=False,
    #     ticket=None,
    #     abstraction='summary',
    #     todo=False,
    #     force=False
    # )
    
    print("\n3. Dry run completed")
    print("   Set dry_run=False to actually execute")
    
    print("\n" + "=" * 60)
    print("Workflow definition ready!")
    print("=" * 60)


def create_minimal_workflow():
    """Create a minimal workflow example."""
    print("\n" + "=" * 60)
    print("Minimal Workflow Example")
    print("=" * 60)
    
    workflow = """
    from goal.push.stages import (
        handle_single_commit,
        handle_version_sync,
        handle_changelog
    )
    from goal.git_ops import run_git
    
    # 1. Stage files
    run_git('add', '-A')
    
    # 2. Update version
    handle_version_sync('1.0.1', no_version_sync=False, 
                       user_config=None, yes=True)
    
    # 3. Update changelog
    handle_changelog('1.0.1', files=['src/main.py'], 
                    commit_msg='feat: new feature', 
                    config=None, no_changelog=False)
    
    # 4. Commit
    handle_single_commit(
        title='feat: new feature',
        body=None,
        commit_msg='feat: new feature',
        message=None,
        yes=True
    )
    """
    
    print(workflow)


if __name__ == "__main__":
    run_custom_workflow()
    create_minimal_workflow()
