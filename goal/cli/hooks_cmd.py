"""Hooks command for pre-commit integration."""

import click

from goal.cli import main
from goal.hooks import HooksManager


@main.group()
def hooks() -> None:
    """Manage pre-commit hooks."""
    pass


@hooks.command(name='install')
@click.option('--force', '-f', is_flag=True, help='Reinstall even if already installed')
def hooks_install(force) -> None:
    """Install Goal pre-commit hooks."""
    manager = HooksManager()
    if manager.install_hooks(force):
        click.echo()
        click.echo(click.style("✓ Pre-commit hooks installed successfully!", fg='green', bold=True))
        click.echo()
        click.echo("Hooks will now run before each commit:")
        click.echo("  • File size validation")
        click.echo("  • API token detection")
        click.echo("  • Dot folder detection")
    else:
        click.echo()
        click.echo(click.style("✗ Installation failed", fg='red'))


@hooks.command(name='uninstall')
def hooks_uninstall() -> None:
    """Uninstall Goal pre-commit hooks."""
    manager = HooksManager()
    if manager.uninstall_hooks():
        click.echo()
        click.echo(click.style("✓ Pre-commit hooks uninstalled", fg='green'))
    else:
        click.echo()
        click.echo(click.style("✗ Uninstallation failed", fg='red'))


@hooks.command(name='run')
@click.option('--all-files', '-a', is_flag=True, help='Run on all files instead of just staged')
def hooks_run(all_files) -> None:
    """Run pre-commit hooks manually."""
    manager = HooksManager()
    if manager.run_hooks(all_files):
        click.echo()
        click.echo(click.style("✓ All hooks passed", fg='green'))
    else:
        click.echo()
        click.echo(click.style("✗ Some hooks failed", fg='red'))


@hooks.command(name='status')
def hooks_status() -> None:
    """Show pre-commit hooks status."""
    manager = HooksManager()
    manager.status()


__all__ = [
    'hooks',
    'hooks_install',
    'hooks_uninstall',
    'hooks_run',
    'hooks_status',
]
