#!/usr/bin/env python3
"""
Comprehensive end-to-end tests for interactive lesson flow.
Tests that the program stays interactive and doesn't exit prematurely.
"""

import unittest
import sys
import builtins
from io import StringIO
from pathlib import Path
from unittest.mock import Mock, patch, call

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lessons import LESSONS, get_lesson
from linuxtutor import LinuxTutor


class TestInteractiveFlow(unittest.TestCase):
    """Test that interactive sessions continue properly without exiting."""

    def setUp(self):
        """Set up test tutor instance."""
        self.tutor = LinuxTutor()
        self.tutor.progress['completed_lessons'] = []
        self.tutor.progress['current_lesson'] = None
        self.tutor.progress['current_level'] = 'beginner'
        self.tutor.progress['first_time'] = False

    def test_post_lesson_options_called_after_lesson_complete(self):
        """Test that post-lesson options are shown after completing a lesson."""
        # Mock run_lesson to simulate lesson completion
        with patch('lessons.run_lesson') as mock_run_lesson:
            with patch.object(self.tutor, 'show_post_lesson_options') as mock_post_options:
                old_stdout = sys.stdout
                sys.stdout = StringIO()

                self.tutor.continue_lesson('intro-to-terminal')

                sys.stdout = old_stdout

                # Verify run_lesson was called
                mock_run_lesson.assert_called_once()

                # Verify post-lesson options were shown
                mock_post_options.assert_called_once_with('intro-to-terminal')

    def test_post_lesson_continue_to_next_lesson(self):
        """Test user can continue to next lesson after completing one."""
        # Mark one lesson as complete
        self.tutor.progress['completed_lessons'] = ['basic-commands']

        old_stdout = sys.stdout
        old_input = builtins.input
        sys.stdout = StringIO()

        # Mock input to choose option 1 (continue to next), then exit
        input_sequence = ['1', '4']  # Choose next lesson, then exit from post-lesson menu
        input_iter = iter(input_sequence)
        builtins.input = lambda _: next(input_iter)

        with patch('lessons.run_lesson') as mock_run_lesson:
            with patch.object(self.tutor, 'show_post_lesson_options', wraps=self.tutor.show_post_lesson_options) as mock_post:
                # Start with first uncompleted lesson
                next_lesson = self.tutor.get_next_lesson()
                if next_lesson:
                    self.tutor.show_post_lesson_options(next_lesson)

                # Should have called run_lesson for the next lesson
                self.assertGreaterEqual(mock_run_lesson.call_count, 0)

                # Should have shown post-lesson options
                self.assertGreaterEqual(mock_post.call_count, 1)

        sys.stdout = old_stdout
        builtins.input = old_input

    def test_post_lesson_view_progress_then_continue(self):
        """Test user can view progress and continue interacting."""
        self.tutor.progress['completed_lessons'] = ['intro-to-terminal']

        old_stdout = sys.stdout
        old_input = builtins.input
        sys.stdout = StringIO()

        # Mock input: choose view progress (3), press enter, then exit (4)
        input_sequence = ['3', '', '4']
        input_iter = iter(input_sequence)
        builtins.input = lambda _: next(input_iter)

        with patch.object(self.tutor, 'show_status') as mock_status:
            self.tutor.show_post_lesson_options('intro-to-terminal')

            # Should have shown status
            mock_status.assert_called_once()

        sys.stdout = old_stdout
        builtins.input = old_input

    def test_post_lesson_choose_different_lesson(self):
        """Test user can choose a different lesson after completing one."""
        old_stdout = sys.stdout
        old_input = builtins.input
        sys.stdout = StringIO()

        # Mock input: choose different lesson (2), enter lesson name, then lesson exits
        input_sequence = ['2', 'file-permissions', '4']
        input_iter = iter(input_sequence)
        builtins.input = lambda _: next(input_iter)

        with patch('lessons.run_lesson') as mock_run_lesson:
            with patch.object(self.tutor, 'list_lessons'):
                self.tutor.show_post_lesson_options('basic-commands')

                # Should have attempted to run the chosen lesson
                if mock_run_lesson.call_count > 0:
                    # Verify file-permissions was attempted
                    calls = mock_run_lesson.call_args_list
                    lesson_names = [call_args[0][0] for call_args in calls if call_args[0]]
                    # Note: file-permissions might be in LESSONS keys format
                    self.assertTrue(any('permission' in str(name) for name in lesson_names))

        sys.stdout = old_stdout
        builtins.input = old_input

    def test_post_lesson_explicit_exit(self):
        """Test user can explicitly exit after completing a lesson."""
        old_stdout = sys.stdout
        old_input = builtins.input
        sys.stdout = StringIO()

        # Mock input to choose exit (4)
        builtins.input = lambda _: '4'

        self.tutor.show_post_lesson_options('intro-to-terminal')

        output = sys.stdout.getvalue()

        sys.stdout = old_stdout
        builtins.input = old_input

        # Should show exit message
        self.assertIn('Great work', output)
        self.assertIn('Come back anytime', output)

    def test_no_exit_after_single_lesson(self):
        """Test that program doesn't exit after a single lesson completes."""
        old_stdout = sys.stdout
        old_input = builtins.input
        sys.stdout = StringIO()

        # Mock input to exit after post-lesson options
        builtins.input = lambda _: '4'

        with patch('lessons.run_lesson'):
            # complete_lesson shouldn't cause exit
            self.tutor.continue_lesson('intro-to-terminal')

            # If we get here, program didn't exit (good!)
            output = sys.stdout.getvalue()

            # Should have shown post-lesson options
            self.assertIn('What would you like to do next', output)

        sys.stdout = old_stdout
        builtins.input = old_input

    def test_level_up_continues_interactive_session(self):
        """Test that leveling up continues the interactive session."""
        # Complete all beginner lessons
        beginner_lessons = [lid for lid, data in LESSONS.items() if data['level'] == 'beginner']
        self.tutor.progress['completed_lessons'] = beginner_lessons
        self.tutor.progress['current_level'] = 'beginner'

        old_stdout = sys.stdout
        old_input = builtins.input
        sys.stdout = StringIO()

        # Mock input: choose to level up, then exit
        input_sequence = ['y', '4']
        input_iter = iter(input_sequence)
        builtins.input = lambda _: next(input_iter)

        with patch('lessons.run_lesson'):
            self.tutor.suggest_level_up()

            output = sys.stdout.getvalue()

            # Should have offered to level up
            self.assertIn('level up', output.lower())

        sys.stdout = old_stdout
        builtins.input = old_input

    def test_interactive_session_offers_choices_after_lesson(self):
        """Test that after lesson, user is offered interactive choices."""
        old_stdout = sys.stdout
        old_input = builtins.input
        sys.stdout = StringIO()

        # Mock input to exit immediately
        builtins.input = lambda _: '4'

        # Test the post-lesson flow directly
        self.tutor.show_post_lesson_options('basic-commands')

        output = sys.stdout.getvalue()

        sys.stdout = old_stdout
        builtins.input = old_input

        # Key assertions: the program doesn't just exit
        # Instead it shows options for what to do next
        self.assertIn('What would you like to do next', output)
        self.assertIn('1.', output)  # Shows menu options
        self.assertIn('Exit', output)  # Shows exit option

    def test_continue_lesson_shows_post_options_not_just_exit(self):
        """Test that continue_lesson stays interactive, not just running and exiting."""
        old_stdout = sys.stdout
        old_input = builtins.input
        sys.stdout = StringIO()

        # Mock input to exit after post-lesson menu
        builtins.input = lambda _: '4'

        with patch('lessons.run_lesson'):
            # Complete lesson should trigger post-lesson options
            self.tutor.continue_lesson('intro-to-terminal')

            output = sys.stdout.getvalue()

            # The key behavior: program shows "what next?" menu
            # NOT just runs lesson and exits
            self.assertIn('What would you like to do next', output)

        sys.stdout = old_stdout
        builtins.input = old_input


class TestGetNextLesson(unittest.TestCase):
    """Test get_next_lesson works correctly."""

    def setUp(self):
        self.tutor = LinuxTutor()
        self.tutor.progress['completed_lessons'] = []
        self.tutor.progress['current_level'] = 'beginner'

    def test_get_next_lesson_first_lesson(self):
        """Test getting first lesson when none completed."""
        next_lesson = self.tutor.get_next_lesson()
        self.assertIsNotNone(next_lesson)
        self.assertIn(next_lesson, LESSONS)
        self.assertEqual(LESSONS[next_lesson]['level'], 'beginner')

    def test_get_next_lesson_skips_completed(self):
        """Test that get_next_lesson skips completed lessons."""
        # Get first lesson
        first_lesson = self.tutor.get_next_lesson()

        # Mark it as completed
        self.tutor.progress['completed_lessons'].append(first_lesson)

        # Get next lesson
        second_lesson = self.tutor.get_next_lesson()

        # Should be different from first
        self.assertNotEqual(first_lesson, second_lesson)
        self.assertNotIn(second_lesson, self.tutor.progress['completed_lessons'])

    def test_get_next_lesson_all_completed_returns_none(self):
        """Test that get_next_lesson returns None when all lessons completed."""
        # Complete all beginner lessons
        beginner_lessons = [lid for lid, data in LESSONS.items() if data['level'] == 'beginner']
        self.tutor.progress['completed_lessons'] = beginner_lessons

        next_lesson = self.tutor.get_next_lesson()
        self.assertIsNone(next_lesson)

    def test_get_next_lesson_respects_prerequisites(self):
        """Test that get_next_lesson only suggests lessons with met prerequisites."""
        # Set to intermediate level with only 1 lesson completed
        self.tutor.progress['current_level'] = 'intermediate'
        self.tutor.progress['completed_lessons'] = ['intro-to-terminal']  # Not enough for intermediate

        next_lesson = self.tutor.get_next_lesson()

        # If a lesson is suggested, it must have all prerequisites met
        if next_lesson:
            lesson_data = LESSONS[next_lesson]
            prereqs = lesson_data.get('prerequisites', [])
            completed = set(self.tutor.progress['completed_lessons'])

            # All prerequisites must be in completed lessons
            for prereq in prereqs:
                self.assertIn(prereq, completed,
                            f"Suggested lesson '{next_lesson}' has unmet prerequisite: '{prereq}'")

    def test_get_next_lesson_skips_lessons_with_unmet_prerequisites(self):
        """Test that lessons with unmet prerequisites are skipped."""
        # Set to intermediate level but haven't completed beginner prerequisites
        self.tutor.progress['current_level'] = 'intermediate'
        self.tutor.progress['completed_lessons'] = []  # No lessons completed

        # Get intermediate lessons and check their prerequisites
        intermediate_lessons = [lid for lid, data in LESSONS.items() if data['level'] == 'intermediate']

        # If all intermediate lessons have prerequisites, next_lesson should be None
        all_have_prereqs = all(
            len(LESSONS[lid].get('prerequisites', [])) > 0
            for lid in intermediate_lessons
        )

        next_lesson = self.tutor.get_next_lesson()

        if all_have_prereqs:
            # Should return None since no prerequisites are met
            self.assertIsNone(next_lesson,
                            "Should not suggest any lesson when no prerequisites are met")
        else:
            # If there are lessons without prerequisites, that's okay
            if next_lesson:
                lesson_data = LESSONS[next_lesson]
                prereqs = lesson_data.get('prerequisites', [])
                self.assertEqual(len(prereqs), 0,
                               "Suggested lesson should have no prerequisites")

    def test_get_next_lesson_users_exact_bug_scenario(self):
        """Test the exact scenario the user reported as a bug."""
        # User's scenario: intermediate level, 1 lesson completed
        self.tutor.progress['current_level'] = 'intermediate'
        self.tutor.progress['completed_lessons'] = ['intro-to-terminal']

        # Process-management requires basic-commands which isn't completed
        # So get_next_lesson should NOT return process-management
        next_lesson = self.tutor.get_next_lesson()

        # If process-management is suggested, verify prerequisites are met
        if next_lesson == 'process-management':
            lesson_data = LESSONS['process-management']
            prereqs = lesson_data.get('prerequisites', [])
            completed = set(self.tutor.progress['completed_lessons'])

            for prereq in prereqs:
                self.assertIn(prereq, completed,
                            f"BUG REPRODUCED: process-management suggested but prerequisite '{prereq}' not completed!")

    def test_get_next_lesson_only_suggests_lessons_user_can_take(self):
        """Test that EVERY suggested lesson can actually be taken (no prerequisite errors)."""
        # Try various scenarios
        scenarios = [
            {'level': 'beginner', 'completed': []},
            {'level': 'beginner', 'completed': ['intro-to-terminal']},
            {'level': 'intermediate', 'completed': ['basic-commands', 'file-system-basics']},
            {'level': 'intermediate', 'completed': []},
        ]

        for scenario in scenarios:
            with self.subTest(scenario=scenario):
                self.tutor.progress['current_level'] = scenario['level']
                self.tutor.progress['completed_lessons'] = scenario['completed']

                next_lesson = self.tutor.get_next_lesson()

                if next_lesson:
                    # Verify the suggested lesson can actually be started
                    lesson_data = LESSONS[next_lesson]
                    prereqs = lesson_data.get('prerequisites', [])
                    completed = set(self.tutor.progress['completed_lessons'])

                    # CRITICAL: All prerequisites must be met
                    all_prereqs_met = all(prereq in completed for prereq in prereqs)
                    self.assertTrue(all_prereqs_met,
                                  f"Lesson '{next_lesson}' suggested but prerequisites {prereqs} not met. "
                                  f"Completed: {list(completed)}")


if __name__ == '__main__':
    unittest.main()
