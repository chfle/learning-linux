#!/usr/bin/env python3
"""
LinuxTutor Test Runner

Automatically discovers and runs all tests in the tests/ directory.
Supports multiple test patterns and provides detailed reporting.

Usage:
    python run_tests.py              # Run all tests
    python run_tests.py -v           # Verbose output
    python run_tests.py --pattern test_*.py  # Custom pattern
    python run_tests.py --help       # Show help
"""

import sys
import unittest
import argparse
from pathlib import Path


def discover_tests(test_dir='tests', pattern='test_*.py'):
    """
    Automatically discover all test files matching the pattern.

    Args:
        test_dir: Directory containing tests (default: 'tests')
        pattern: Pattern to match test files (default: 'test_*.py')

    Returns:
        TestSuite containing all discovered tests
    """
    loader = unittest.TestLoader()
    start_dir = Path(__file__).parent / test_dir

    if not start_dir.exists():
        print(f"Error: Test directory '{test_dir}' not found", file=sys.stderr)
        return unittest.TestSuite()

    # Discover tests
    suite = loader.discover(
        start_dir=str(start_dir),
        pattern=pattern,
        top_level_dir=str(Path(__file__).parent)
    )

    return suite


def count_tests(suite):
    """Count total number of tests in a test suite."""
    count = 0
    for test in suite:
        if isinstance(test, unittest.TestSuite):
            count += count_tests(test)
        else:
            count += 1
    return count


def run_tests(verbosity=1, pattern='test_*.py', failfast=False):
    """
    Run all discovered tests with specified options.

    Args:
        verbosity: Output verbosity (0=quiet, 1=normal, 2=verbose)
        pattern: Test file pattern to match
        failfast: Stop on first failure

    Returns:
        True if all tests passed, False otherwise
    """
    # Discover tests
    print(f"Discovering tests with pattern: {pattern}")
    suite = discover_tests(pattern=pattern)

    # Count tests
    test_count = count_tests(suite)
    if test_count == 0:
        print(f"No tests found matching pattern '{pattern}'", file=sys.stderr)
        return False

    print(f"Found {test_count} tests\n")

    # Run tests
    runner = unittest.TextTestRunner(
        verbosity=verbosity,
        failfast=failfast,
        stream=sys.stdout
    )

    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print("=" * 70)

    return result.wasSuccessful()


def main():
    """Main entry point for the test runner."""
    parser = argparse.ArgumentParser(
        description='LinuxTutor Test Runner - Automatically discover and run tests',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_tests.py              # Run all tests
  python run_tests.py -v           # Verbose output
  python run_tests.py -vv          # Very verbose output
  python run_tests.py --pattern "test_search.py"  # Run specific test file
  python run_tests.py --failfast   # Stop on first failure
        """
    )

    parser.add_argument(
        '-v', '--verbose',
        action='count',
        default=1,
        help='Increase verbosity (use -v or -vv)'
    )

    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Minimal output'
    )

    parser.add_argument(
        '--pattern',
        default='test_*.py',
        help='Pattern to match test files (default: test_*.py)'
    )

    parser.add_argument(
        '--failfast',
        action='store_true',
        help='Stop on first failure'
    )

    args = parser.parse_args()

    # Determine verbosity
    if args.quiet:
        verbosity = 0
    else:
        verbosity = args.verbose

    # Run tests
    try:
        success = run_tests(
            verbosity=verbosity,
            pattern=args.pattern,
            failfast=args.failfast
        )
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest run interrupted by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"\nError running tests: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
