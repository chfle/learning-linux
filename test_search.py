#!/usr/bin/env python3

import unittest
import sys
from io import StringIO
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent))

from lessons import (
    _extract_snippet,
    _calculate_score,
    _search_in_lesson,
    search_lessons,
    LESSONS
)
from linuxtutor import LinuxTutor


class TestExtractSnippet(unittest.TestCase):
    """Test the _extract_snippet helper function."""

    def test_basic_snippet(self):
        """Test basic snippet extraction."""
        text = "This is a test of the snippet extraction functionality."
        result = _extract_snippet(text, "snippet", context_chars=10)
        self.assertIn("snippet", result)
        # Check that some context is included
        self.assertGreater(len(result), len("snippet"))

    def test_snippet_with_ellipsis_start(self):
        """Test snippet with ellipsis at start."""
        text = "A" * 100 + "keyword" + "B" * 100
        result = _extract_snippet(text, "keyword", context_chars=10)
        self.assertTrue(result.startswith("..."))
        self.assertIn("keyword", result)

    def test_snippet_with_ellipsis_end(self):
        """Test snippet with ellipsis at end."""
        text = "A" * 100 + "keyword" + "B" * 100
        result = _extract_snippet(text, "keyword", context_chars=10)
        self.assertTrue(result.endswith("..."))
        self.assertIn("keyword", result)

    def test_case_insensitive_snippet(self):
        """Test case-insensitive snippet extraction."""
        text = "This contains KEYWORD in uppercase."
        result = _extract_snippet(text, "keyword", context_chars=15)
        self.assertIn("KEYWORD", result)

    def test_keyword_not_found(self):
        """Test snippet when keyword is not found."""
        text = "This text does not contain the search term."
        result = _extract_snippet(text, "missing", context_chars=10)
        self.assertEqual(result, "")

    def test_snippet_at_start(self):
        """Test snippet extraction when keyword is at start."""
        text = "keyword at the beginning of text"
        result = _extract_snippet(text, "keyword", context_chars=10)
        self.assertFalse(result.startswith("..."))
        self.assertIn("keyword", result)

    def test_snippet_at_end(self):
        """Test snippet extraction when keyword is at end."""
        text = "text with keyword"
        result = _extract_snippet(text, "keyword", context_chars=10)
        self.assertFalse(result.endswith("..."))
        self.assertIn("keyword", result)


class TestCalculateScore(unittest.TestCase):
    """Test the _calculate_score helper function."""

    def test_title_match_highest_score(self):
        """Test that title matches have highest score."""
        matches = {'title': 1}
        score = _calculate_score(matches)
        self.assertEqual(score, 10)

    def test_description_match(self):
        """Test description match score."""
        matches = {'description': 1}
        score = _calculate_score(matches)
        self.assertEqual(score, 5)

    def test_text_match_lowest_score(self):
        """Test text matches have lowest score."""
        matches = {'text': 1}
        score = _calculate_score(matches)
        self.assertEqual(score, 1)

    def test_multiple_matches(self):
        """Test scoring with multiple match types."""
        matches = {
            'title': 1,
            'description': 1,
            'text': 2
        }
        score = _calculate_score(matches)
        self.assertEqual(score, 10 + 5 + 2)  # 17

    def test_multiple_occurrences(self):
        """Test scoring with multiple occurrences of same field."""
        matches = {'title': 3}
        score = _calculate_score(matches)
        self.assertEqual(score, 30)

    def test_empty_matches(self):
        """Test scoring with no matches."""
        matches = {}
        score = _calculate_score(matches)
        self.assertEqual(score, 0)


class TestSearchInLesson(unittest.TestCase):
    """Test the _search_in_lesson helper function."""

    def setUp(self):
        """Set up test lesson data."""
        self.lesson = {
            'title': 'Test Lesson About Files',
            'level': 'beginner',
            'duration': 20,
            'description': 'Learn about file management and security.',
            'prerequisites': [],
            'content': [
                {
                    'type': 'explanation',
                    'title': 'File System Basics',
                    'text': 'The file system is where all your files are stored.'
                },
                {
                    'type': 'exercise',
                    'title': 'Practice with Files',
                    'instructions': 'Try these file commands.',
                    'commands': [
                        {'cmd': 'ls -la', 'description': 'List all files in directory'},
                        {'cmd': 'cat file.txt', 'description': 'Display file contents'}
                    ]
                }
            ]
        }

    def test_single_keyword_match_in_title(self):
        """Test single keyword matching in title."""
        result = _search_in_lesson(self.lesson, ['files'])
        self.assertIsNotNone(result)
        self.assertIn('title', result['fields_matched'])
        self.assertGreater(result['score'], 0)

    def test_single_keyword_match_in_description(self):
        """Test single keyword matching in description."""
        result = _search_in_lesson(self.lesson, ['security'])
        self.assertIsNotNone(result)
        self.assertIn('description', result['fields_matched'])

    def test_multiple_keywords_and_logic(self):
        """Test AND logic - all keywords must match."""
        result = _search_in_lesson(self.lesson, ['file', 'security'])
        self.assertIsNotNone(result)

    def test_multiple_keywords_and_logic_fail(self):
        """Test AND logic failure - missing keyword."""
        result = _search_in_lesson(self.lesson, ['file', 'missing'])
        self.assertIsNone(result)

    def test_case_insensitive_search(self):
        """Test case-insensitive search."""
        result = _search_in_lesson(self.lesson, ['FILE'])
        self.assertIsNotNone(result)

    def test_match_in_section_title(self):
        """Test matching in content section title."""
        result = _search_in_lesson(self.lesson, ['basics'])
        self.assertIsNotNone(result)
        self.assertIn('section_title', result['fields_matched'])

    def test_match_in_text(self):
        """Test matching in explanation text."""
        result = _search_in_lesson(self.lesson, ['stored'])
        self.assertIsNotNone(result)
        self.assertIn('text', result['fields_matched'])

    def test_match_in_command(self):
        """Test matching in command."""
        result = _search_in_lesson(self.lesson, ['ls'])
        self.assertIsNotNone(result)
        self.assertIn('command', result['fields_matched'])

    def test_match_in_command_description(self):
        """Test matching in command description."""
        result = _search_in_lesson(self.lesson, ['directory'])
        self.assertIsNotNone(result)
        self.assertIn('command_desc', result['fields_matched'])

    def test_snippet_extraction(self):
        """Test that snippets are extracted."""
        result = _search_in_lesson(self.lesson, ['security'])
        self.assertIsNotNone(result)
        self.assertIn('snippets', result)
        self.assertTrue(len(result['snippets']) > 0)

    def test_no_match(self):
        """Test when no keywords match."""
        result = _search_in_lesson(self.lesson, ['nonexistent'])
        self.assertIsNone(result)


class TestSearchLessons(unittest.TestCase):
    """Test the search_lessons public API function."""

    def test_single_keyword_search(self):
        """Test search with single keyword."""
        results = search_lessons(['file'])
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        # Verify all results contain the keyword
        for result in results:
            self.assertIn('lesson_id', result)
            self.assertIn('lesson_data', result)
            self.assertIn('score', result)

    def test_multiple_keyword_search(self):
        """Test search with multiple keywords (AND logic)."""
        results = search_lessons(['file', 'system'])
        self.assertIsInstance(results, list)
        # All results should contain both keywords
        for result in results:
            self.assertGreater(result['score'], 0)

    def test_case_insensitive_search(self):
        """Test case-insensitive search."""
        results_lower = search_lessons(['process'])
        results_upper = search_lessons(['PROCESS'])
        self.assertEqual(len(results_lower), len(results_upper))

    def test_results_sorted_by_score(self):
        """Test that results are sorted by score (descending)."""
        results = search_lessons(['linux'])
        if len(results) > 1:
            for i in range(len(results) - 1):
                self.assertGreaterEqual(results[i]['score'], results[i + 1]['score'])

    def test_no_results(self):
        """Test search with no matching results."""
        results = search_lessons(['xyznonexistent'])
        self.assertEqual(len(results), 0)

    def test_and_logic_strict(self):
        """Test AND logic - missing one keyword returns no results."""
        results = search_lessons(['file', 'xyznonexistent'])
        self.assertEqual(len(results), 0)

    def test_search_finds_beginner_lessons(self):
        """Test search finds beginner level lessons."""
        results = search_lessons(['terminal'])
        beginner_results = [r for r in results if r['lesson_data']['level'] == 'beginner']
        self.assertGreater(len(beginner_results), 0)

    def test_search_finds_advanced_lessons(self):
        """Test search finds advanced level lessons."""
        results = search_lessons(['security'])
        advanced_results = [r for r in results if r['lesson_data']['level'] == 'advanced']
        self.assertGreater(len(advanced_results), 0)


class TestRelevanceScoring(unittest.TestCase):
    """Test relevance scoring and ranking."""

    def test_title_match_scores_higher(self):
        """Test that title matches score higher than description matches."""
        # Search for a term that appears in titles
        results = search_lessons(['performance'])
        if len(results) > 0:
            # Lessons with term in title should score higher
            for result in results:
                if 'title' in result['fields_matched']:
                    self.assertGreater(result['score'], 5)

    def test_multiple_matches_increase_score(self):
        """Test that multiple matches increase score."""
        results = search_lessons(['file'])
        if len(results) >= 2:
            # Results with more matches should have higher scores
            scores = [r['score'] for r in results]
            self.assertTrue(any(s1 != s2 for s1, s2 in zip(scores, scores[1:])))


class TestLinuxTutorSearchMethod(unittest.TestCase):
    """Test the LinuxTutor.search_lessons method."""

    def setUp(self):
        """Set up LinuxTutor instance for testing."""
        self.tutor = LinuxTutor()

    def test_search_lessons_method_exists(self):
        """Test that search_lessons method exists."""
        self.assertTrue(hasattr(self.tutor, 'search_lessons'))

    def test_search_with_keywords(self):
        """Test search with valid keywords."""
        # Capture stdout
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        self.tutor.search_lessons(['file'])

        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        # Should have output
        self.assertGreater(len(output), 0)
        self.assertIn('Found', output)

    def test_search_with_level_filter(self):
        """Test search with level filter."""
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        self.tutor.search_lessons(['linux'], level_filter='beginner')

        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        # Should filter to beginner level
        if 'Found' in output:
            self.assertIn('[Beginner]', output)

    def test_search_no_results(self):
        """Test search with no results."""
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        self.tutor.search_lessons(['xyznonexistent'])

        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        self.assertIn('No lessons found', output)

    def test_search_empty_keywords(self):
        """Test search with empty keyword list."""
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        self.tutor.search_lessons([])

        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        self.assertIn('Error', output)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""

    def test_special_characters_in_keyword(self):
        """Test search with special characters."""
        results = search_lessons(['file-system'])
        # Should handle hyphens gracefully
        self.assertIsInstance(results, list)

    def test_very_long_keyword(self):
        """Test search with very long keyword."""
        long_keyword = 'a' * 1000
        results = search_lessons([long_keyword])
        self.assertEqual(len(results), 0)

    def test_empty_string_keyword(self):
        """Test search with empty string keyword."""
        results = search_lessons([''])
        # Should handle gracefully
        self.assertIsInstance(results, list)

    def test_single_character_keyword(self):
        """Test search with single character."""
        results = search_lessons(['a'])
        # Should return results if 'a' appears in lessons
        self.assertIsInstance(results, list)

    def test_numeric_keyword(self):
        """Test search with numeric keyword."""
        results = search_lessons(['123'])
        self.assertIsInstance(results, list)


class TestIntegration(unittest.TestCase):
    """Integration tests for the search feature."""

    def test_search_all_lesson_levels(self):
        """Test that search can find lessons at all levels."""
        all_results = search_lessons(['linux'])
        if len(all_results) > 0:
            levels_found = set(r['lesson_data']['level'] for r in all_results)
            # Should find at least one level
            self.assertGreater(len(levels_found), 0)

    def test_search_results_have_all_fields(self):
        """Test that search results have all required fields."""
        results = search_lessons(['file'])
        if len(results) > 0:
            result = results[0]
            self.assertIn('lesson_id', result)
            self.assertIn('lesson_data', result)
            self.assertIn('score', result)
            self.assertIn('fields_matched', result)
            self.assertIn('snippets', result)

    def test_search_performance_acceptable(self):
        """Test that search completes in reasonable time."""
        import time
        start = time.time()
        search_lessons(['test'])
        elapsed = time.time() - start
        # Should complete in less than 1 second
        self.assertLess(elapsed, 1.0)


def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestExtractSnippet))
    suite.addTests(loader.loadTestsFromTestCase(TestCalculateScore))
    suite.addTests(loader.loadTestsFromTestCase(TestSearchInLesson))
    suite.addTests(loader.loadTestsFromTestCase(TestSearchLessons))
    suite.addTests(loader.loadTestsFromTestCase(TestRelevanceScoring))
    suite.addTests(loader.loadTestsFromTestCase(TestLinuxTutorSearchMethod))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Return success status
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
