"""Goal validators package - security and file validation.

This package provides validation for files before commit,
including file size limits, API token detection, and proactive .gitignore management.
"""

from .file_validator import (
    validate_files,
    validate_staged_files,
    ValidationError,
    FileSizeError,
    TokenDetectedError,
    DotFolderError,
    manage_dot_folders,
)

__all__ = [
    'validate_files',
    'validate_staged_files',
    'ValidationError',
    'FileSizeError',
    'TokenDetectedError',
    'DotFolderError',
    'manage_dot_folders',
]
