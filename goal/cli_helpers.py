"""Shared CLI helpers that are safe to import from workflow packages."""

import os
from typing import Dict, List

import click

from goal.git_ops import run_git


def split_paths_by_type(paths: List[str]) -> Dict[str, List[str]]:
    """Split file paths into groups (code/docs/ci/examples/other)."""
    groups: Dict[str, List[str]] = {'code': [], 'docs': [], 'ci': [], 'examples': [], 'other': []}
    for p in paths:
        pl = p.lower()
        if pl.startswith('examples/'):
            groups['examples'].append(p)
        elif pl.startswith('docs/') or pl.endswith(('.md', '.rst')) or os.path.basename(pl) in ('readme.md',):
            groups['docs'].append(p)
        elif pl.startswith('.github/') or pl.startswith('.gitlab/') or pl.endswith(('.yml', '.yaml')):
            groups['ci'].append(p)
        elif pl.startswith('src/') or pl.startswith('lib/') or pl.endswith('.py'):
            groups['code'].append(p)
        else:
            groups['other'].append(p)

    return {k: v for k, v in groups.items() if v}


def stage_paths(paths: List[str]) -> None:
    if not paths:
        return
    # stage in chunks to avoid arg length issues
    chunk: List[str] = []
    for p in paths:
        chunk.append(p)
        if len(chunk) >= 100:
            run_git('add', '--', *chunk)
            chunk = []
    if chunk:
        run_git('add', '--', *chunk)


def confirm(prompt: str, default: bool = True) -> bool:
    """Ask for user confirmation with Y/n prompt (Enter defaults to Yes)."""
    if default:
        suffix = " [Y/n] "
    else:
        suffix = " [y/N] "

    while True:
        response = input(f"{click.style(prompt, fg='cyan')}{suffix}").strip().lower()

        if not response:
            return default

        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            click.echo(click.style("Please respond with 'y' or 'n'", fg='red'))


__all__ = ['split_paths_by_type', 'stage_paths', 'confirm']
