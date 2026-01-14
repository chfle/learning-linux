#!/usr/bin/env python3
"""
Python Syntax Validator

Automatically discovers and validates syntax for all Python files in the project.
Useful for CI/CD pipelines and pre-commit checks.

Usage:
    python validate_syntax.py              # Validate all Python files
    python validate_syntax.py --verbose    # Show all files being checked
    python validate_syntax.py --exclude tests  # Exclude directory
"""

import sys
import py_compile
import argparse
from pathlib import Path


def find_python_files(root_dir='.', exclude_dirs=None):
    """
    Recursively find all Python files in the project.

    Args:
        root_dir: Root directory to search (default: current directory)
        exclude_dirs: List of directory names to exclude

    Returns:
        List of Path objects for Python files
    """
    if exclude_dirs is None:
        exclude_dirs = ['__pycache__', '.git', '.github', 'venv', 'env', '.venv']

    root = Path(root_dir).resolve()
    python_files = []

    for path in root.rglob('*.py'):
        # Check if any parent directory is in exclude list
        if any(excluded in path.parts for excluded in exclude_dirs):
            continue
        python_files.append(path)

    return sorted(python_files)


def validate_file(file_path, verbose=False):
    """
    Validate Python syntax for a single file.

    Args:
        file_path: Path to Python file
        verbose: Print success messages

    Returns:
        True if valid, False if syntax error
    """
    try:
        py_compile.compile(str(file_path), doraise=True)
        if verbose:
            print(f"✓ {file_path}")
        return True
    except py_compile.PyCompileError as e:
        print(f"✗ {file_path}")
        print(f"  Syntax Error: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"✗ {file_path}")
        print(f"  Error: {e}", file=sys.stderr)
        return False


def validate_all(root_dir='.', exclude_dirs=None, verbose=False):
    """
    Validate all Python files in the project.

    Args:
        root_dir: Root directory to search
        exclude_dirs: List of directories to exclude
        verbose: Print all files being checked

    Returns:
        Tuple of (success_count, fail_count, total_count)
    """
    python_files = find_python_files(root_dir, exclude_dirs)

    if not python_files:
        print("No Python files found", file=sys.stderr)
        return 0, 0, 0

    print(f"Validating {len(python_files)} Python files...\n")

    success_count = 0
    fail_count = 0

    for file_path in python_files:
        if validate_file(file_path, verbose):
            success_count += 1
        else:
            fail_count += 1

    return success_count, fail_count, len(python_files)


def main():
    """Main entry point for the syntax validator."""
    parser = argparse.ArgumentParser(
        description='Validate Python syntax for all files in the project',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python validate_syntax.py                      # Validate all Python files
  python validate_syntax.py -v                   # Verbose output
  python validate_syntax.py --exclude tests venv # Exclude directories
        """
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show all files being validated'
    )

    parser.add_argument(
        '--exclude',
        nargs='+',
        default=['__pycache__', '.git', '.github', 'venv', 'env', '.venv'],
        help='Directories to exclude (default: __pycache__ .git .github venv env .venv)'
    )

    parser.add_argument(
        '--dir',
        default='.',
        help='Root directory to search (default: current directory)'
    )

    args = parser.parse_args()

    try:
        success, fail, total = validate_all(
            root_dir=args.dir,
            exclude_dirs=args.exclude,
            verbose=args.verbose
        )

        print("\n" + "=" * 70)
        print("VALIDATION SUMMARY")
        print("=" * 70)
        print(f"Total files: {total}")
        print(f"Valid: {success} ✓")
        print(f"Invalid: {fail} ✗")
        print("=" * 70)

        if fail > 0:
            print("\n❌ Syntax validation FAILED", file=sys.stderr)
            sys.exit(1)
        else:
            print("\n✅ All Python files have valid syntax")
            sys.exit(0)

    except KeyboardInterrupt:
        print("\n\nValidation interrupted by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"\nError during validation: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
