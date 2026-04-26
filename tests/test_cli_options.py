import subprocess
from click.testing import CliRunner

from goal.cli import main


def run_cli(*args):
    return subprocess.run(['python3', '-m', 'goal', *args], capture_output=True, text=True)


def test_push_help_includes_markdown_ascii_split_ticket() -> None:
    res = run_cli('push', '--help')
    assert res.returncode == 0
    out = res.stdout
    assert '--markdown / --ascii' in out
    assert '--split' in out
    assert '--ticket' in out


def test_status_help_includes_markdown_ascii() -> None:
    res = run_cli('status', '--help')
    assert res.returncode == 0
    assert '--markdown / --ascii' in res.stdout


def test_unknown_command_shows_docs_url() -> None:
    res = run_cli('nonexistent_command')
    assert res.returncode == 2
    out = res.output if hasattr(res, 'output') else res.stdout + res.stderr
    assert 'does not exist' in out.lower() or 'not exist' in out.lower()
    assert 'github.com/wronai/goal' in out or 'Documentation:' in out


def test_known_commands_work() -> None:
    res = run_cli('--help')
    assert res.returncode == 0
    assert 'Usage:' in res.stdout


def test_all_help_does_not_fail_when_push_unavailable() -> None:
    runner = CliRunner()
    push_cmd = main.commands.pop('push', None)
    try:
        res = runner.invoke(main, ['-a', '--help'])
    finally:
        if push_cmd is not None:
            main.commands['push'] = push_cmd

    assert res.exit_code == 0
    assert 'Usage:' in res.output


def test_missing_push_command_shows_install_hint() -> None:
    runner = CliRunner()
    push_cmd = main.commands.pop('push', None)
    try:
        res = runner.invoke(main, ['push'])
    finally:
        if push_cmd is not None:
            main.commands['push'] = push_cmd

    assert res.exit_code == 2
    assert 'push' in res.output.lower()
    assert 'force-reinstall' in res.output