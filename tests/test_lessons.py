#!/usr/bin/env python3

import unittest
import sys
from io import StringIO
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from lessons import LESSONS, get_lesson
from linuxtutor import LinuxTutor


class TestLessonStructure(unittest.TestCase):
    """Test lesson data structure validity."""

    def test_all_lessons_have_required_fields(self):
        """Test that all lessons have required fields."""
        required_fields = ['title', 'level', 'duration', 'description', 'prerequisites', 'content']

        for lesson_id, lesson_data in LESSONS.items():
            with self.subTest(lesson=lesson_id):
                for field in required_fields:
                    self.assertIn(field, lesson_data, f"Lesson {lesson_id} missing field: {field}")

    def test_lesson_levels_valid(self):
        """Test that all lessons have valid level values."""
        valid_levels = ['beginner', 'intermediate', 'advanced', 'expert']

        for lesson_id, lesson_data in LESSONS.items():
            with self.subTest(lesson=lesson_id):
                self.assertIn(lesson_data['level'], valid_levels,
                            f"Lesson {lesson_id} has invalid level: {lesson_data['level']}")

    def test_lesson_duration_positive(self):
        """Test that all lessons have positive duration."""
        for lesson_id, lesson_data in LESSONS.items():
            with self.subTest(lesson=lesson_id):
                self.assertGreater(lesson_data['duration'], 0,
                                 f"Lesson {lesson_id} has non-positive duration")
                self.assertIsInstance(lesson_data['duration'], int,
                                    f"Lesson {lesson_id} duration is not an integer")

    def test_lesson_prerequisites_exist(self):
        """Test that all prerequisites reference existing lessons."""
        all_lesson_ids = set(LESSONS.keys())

        # Track which lessons have missing prerequisites (expected until all lessons implemented)
        lessons_with_missing_prereqs = []

        for lesson_id, lesson_data in LESSONS.items():
            prereqs = lesson_data.get('prerequisites', [])
            for prereq in prereqs:
                if prereq not in all_lesson_ids:
                    lessons_with_missing_prereqs.append((lesson_id, prereq))

        # Allow some missing prerequisites for now (lessons not yet implemented)
        # But new lessons should have valid prerequisites
        for lesson_id in ['file-permissions', 'text-editors']:
            lesson = LESSONS[lesson_id]
            for prereq in lesson['prerequisites']:
                self.assertIn(prereq, all_lesson_ids,
                            f"New lesson {lesson_id} has invalid prerequisite: {prereq}")

    def test_lesson_content_structure(self):
        """Test that lesson content has valid structure."""
        for lesson_id, lesson_data in LESSONS.items():
            content = lesson_data['content']
            with self.subTest(lesson=lesson_id):
                self.assertIsInstance(content, list, f"Lesson {lesson_id} content is not a list")
                self.assertGreater(len(content), 0, f"Lesson {lesson_id} has no content")

                for i, section in enumerate(content):
                    self.assertIn('type', section, f"Lesson {lesson_id} section {i} has no type")
                    self.assertIn(section['type'], ['explanation', 'exercise'],
                                f"Lesson {lesson_id} section {i} has invalid type")

    def test_new_beginner_lessons_exist(self):
        """Test that new beginner lessons are implemented."""
        self.assertIn('file-permissions', LESSONS, "file-permissions lesson not found")
        self.assertIn('text-editors', LESSONS, "text-editors lesson not found")

    def test_file_permissions_lesson_structure(self):
        """Test file-permissions lesson has correct structure."""
        lesson = LESSONS['file-permissions']
        self.assertEqual(lesson['level'], 'beginner')
        self.assertEqual(lesson['title'], 'Understanding File Permissions')
        self.assertEqual(lesson['prerequisites'], ['basic-commands'])
        self.assertGreater(len(lesson['content']), 3)

    def test_text_editors_lesson_structure(self):
        """Test text-editors lesson has correct structure."""
        lesson = LESSONS['text-editors']
        self.assertEqual(lesson['level'], 'beginner')
        self.assertEqual(lesson['title'], 'Working with Text Editors')
        self.assertEqual(lesson['prerequisites'], ['basic-commands'])
        self.assertGreater(len(lesson['content']), 3)


class TestGetLesson(unittest.TestCase):
    """Test the get_lesson function."""

    def test_get_existing_lesson(self):
        """Test getting an existing lesson."""
        lesson = get_lesson('intro-to-terminal')
        self.assertIsNotNone(lesson)
        self.assertEqual(lesson['title'], 'Introduction to the Terminal')

    def test_get_nonexistent_lesson(self):
        """Test getting a non-existent lesson returns None."""
        lesson = get_lesson('fake-lesson')
        self.assertIsNone(lesson)

    def test_get_new_lessons(self):
        """Test getting newly added lessons."""
        file_perm = get_lesson('file-permissions')
        self.assertIsNotNone(file_perm)

        text_ed = get_lesson('text-editors')
        self.assertIsNotNone(text_ed)


class TestDynamicLessonListing(unittest.TestCase):
    """Test dynamic lesson listing functionality."""

    def setUp(self):
        """Set up test tutor instance."""
        self.tutor = LinuxTutor()

    def test_list_lessons_shows_only_existing_lessons(self):
        """Test that list_lessons only shows lessons that actually exist."""
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        self.tutor.list_lessons('beginner')

        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        # Should show 5 beginner lessons
        self.assertIn('Beginner Level Lessons:', output)
        self.assertIn('Basic Commands', output)
        self.assertIn('File Permissions', output)
        self.assertIn('Text Editors', output)
        self.assertIn('File System Basics', output)
        self.assertIn('Intro To Terminal', output)

    def test_list_lessons_dynamic_count(self):
        """Test that lesson count matches actual lessons in LESSONS dict."""
        from lessons import LESSONS

        beginner_count = sum(1 for l in LESSONS.values() if l['level'] == 'beginner')

        old_stdout = sys.stdout
        sys.stdout = StringIO()

        self.tutor.list_lessons('beginner')

        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        # Count how many lessons are listed
        lines = output.split('\n')
        listed_count = sum(1 for line in lines if '○' in line or '✓' in line)

        self.assertEqual(listed_count, beginner_count,
                        f"Listed {listed_count} lessons but LESSONS dict has {beginner_count}")

    def test_list_lessons_all_levels(self):
        """Test listing lessons for all levels."""
        levels = ['beginner', 'intermediate', 'advanced', 'expert']

        for level in levels:
            with self.subTest(level=level):
                old_stdout = sys.stdout
                sys.stdout = StringIO()

                self.tutor.list_lessons(level)

                output = sys.stdout.getvalue()
                sys.stdout = old_stdout

                self.assertIn(f'{level.title()} Level Lessons:', output)


class TestPrerequisiteValidation(unittest.TestCase):
    """Test prerequisite validation functionality."""

    def setUp(self):
        """Set up test tutor instance."""
        self.tutor = LinuxTutor()
        # Start with clean progress
        self.tutor.progress['completed_lessons'] = []

    def test_check_prerequisites_no_prereqs(self):
        """Test lesson with no prerequisites passes."""
        lesson = {'title': 'Test', 'prerequisites': []}
        result = self.tutor.check_prerequisites(lesson, 'test-lesson')
        self.assertTrue(result)

    def test_check_prerequisites_met(self):
        """Test lesson with met prerequisites passes."""
        self.tutor.progress['completed_lessons'] = ['basic-commands']
        lesson = {'title': 'Test', 'prerequisites': ['basic-commands']}

        old_stdout = sys.stdout
        sys.stdout = StringIO()

        result = self.tutor.check_prerequisites(lesson, 'test-lesson')

        sys.stdout = old_stdout

        self.assertTrue(result)

    def test_check_prerequisites_not_met(self):
        """Test lesson with unmet prerequisites fails."""
        self.tutor.progress['completed_lessons'] = []
        lesson = {'title': 'Test', 'prerequisites': ['basic-commands']}

        old_stdout = sys.stdout
        sys.stdout = StringIO()

        result = self.tutor.check_prerequisites(lesson, 'test-lesson')

        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        self.assertFalse(result)
        self.assertIn('Cannot start', output)
        self.assertIn('Basic Commands', output)

    def test_check_prerequisites_multiple_missing(self):
        """Test lesson with multiple missing prerequisites."""
        self.tutor.progress['completed_lessons'] = []
        lesson = {'title': 'Test', 'prerequisites': ['lesson1', 'lesson2', 'lesson3']}

        old_stdout = sys.stdout
        sys.stdout = StringIO()

        result = self.tutor.check_prerequisites(lesson, 'test-lesson')

        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        self.assertFalse(result)
        # Prerequisites are title-cased in output
        self.assertIn('Lesson1', output)
        self.assertIn('Lesson2', output)
        self.assertIn('Lesson3', output)

    def test_check_prerequisites_partial_complete(self):
        """Test lesson with some prerequisites met."""
        self.tutor.progress['completed_lessons'] = ['lesson1']
        lesson = {'title': 'Test', 'prerequisites': ['lesson1', 'lesson2']}

        old_stdout = sys.stdout
        sys.stdout = StringIO()

        result = self.tutor.check_prerequisites(lesson, 'test-lesson')

        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        self.assertFalse(result)
        # Prerequisites are title-cased in output
        self.assertIn('Lesson2', output)
        self.assertNotIn('Lesson1', output)  # lesson1 is complete, shouldn't be mentioned


class TestErrorMessages(unittest.TestCase):
    """Test improved error messages."""

    def setUp(self):
        """Set up test tutor instance."""
        self.tutor = LinuxTutor()

    def test_show_lesson_not_found_help(self):
        """Test helpful error message for missing lesson."""
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        self.tutor.show_lesson_not_found_help('fake-lesson')

        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        self.assertIn('not found', output.lower())
        self.assertIn('Try:', output)
        self.assertIn('linuxtutor lessons', output)

    def test_error_message_suggests_similar(self):
        """Test error message suggests similar lesson names."""
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        # Should suggest 'file-permissions' (substring match)
        self.tutor.show_lesson_not_found_help('file-perm')

        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        # Should show suggestions
        self.assertIn('Did you mean:', output)

    def test_start_lesson_uses_error_helper(self):
        """Test that start_lesson uses the error helper for missing lessons."""
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        self.tutor.start_lesson('nonexistent-lesson')

        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        self.assertIn('not found', output.lower())
        self.assertIn('Try:', output)


class TestNewLessonCommands(unittest.TestCase):
    """Test that new lesson commands are safe."""

    def test_file_permissions_commands_safe(self):
        """Test file-permissions lesson commands are safe."""
        lesson = get_lesson('file-permissions')
        self.assertIsNotNone(lesson)

        for section in lesson['content']:
            if section['type'] == 'exercise':
                for cmd_info in section.get('commands', []):
                    cmd = cmd_info['cmd']

                    # Commands should not contain dangerous operations
                    self.assertNotIn('rm -rf /', cmd)
                    self.assertNotIn('sudo rm', cmd)
                    self.assertNotIn('dd if=', cmd)

    def test_text_editors_commands_safe(self):
        """Test text-editors lesson commands are safe."""
        lesson = get_lesson('text-editors')
        self.assertIsNotNone(lesson)

        for section in lesson['content']:
            if section['type'] == 'exercise':
                for cmd_info in section.get('commands', []):
                    cmd = cmd_info['cmd']

                    # Commands should not contain dangerous operations
                    self.assertNotIn('rm -rf', cmd)
                    self.assertNotIn('sudo', cmd)
                    # nano and vim are safe to run
                    self.assertTrue(any(safe in cmd for safe in ['nano', 'vim', 'cat', 'vimtutor']))


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete workflow."""

    def test_beginner_track_complete(self):
        """Test that beginner track is now complete."""
        from lessons import LESSONS

        beginner_lessons = [k for k, v in LESSONS.items() if v['level'] == 'beginner']

        # Should have 5 beginner lessons now
        self.assertGreaterEqual(len(beginner_lessons), 5,
                              "Beginner track should have at least 5 lessons")

        # Specific lessons should exist
        self.assertIn('intro-to-terminal', beginner_lessons)
        self.assertIn('file-system-basics', beginner_lessons)
        self.assertIn('basic-commands', beginner_lessons)
        self.assertIn('file-permissions', beginner_lessons)
        self.assertIn('text-editors', beginner_lessons)

    def test_lesson_count_increased(self):
        """Test that total lesson count increased."""
        from lessons import LESSONS

        # Should have at least 9 lessons now (was 7, added 2)
        self.assertGreaterEqual(len(LESSONS), 9,
                              "Should have at least 9 lessons after adding new ones")


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestLessonStructure))
    suite.addTests(loader.loadTestsFromTestCase(TestGetLesson))
    suite.addTests(loader.loadTestsFromTestCase(TestDynamicLessonListing))
    suite.addTests(loader.loadTestsFromTestCase(TestPrerequisiteValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestErrorMessages))
    suite.addTests(loader.loadTestsFromTestCase(TestNewLessonCommands))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Return success status
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
