"""
Integration tests for quiz system with lessons and progress tracking.

Tests the complete quiz workflow including:
- Quiz data validation across all lessons
- Lesson completion with quiz requirements
- Progress tracking and statistics
- Backward compatibility with old progress files
"""

import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import tempfile
import json
from pathlib import Path
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from quiz_system import Quiz, QuizRunner
from lessons import LESSONS, run_lesson
from progress_manager import ProgressManager
from linuxtutor import LinuxTutor


class TestQuizDataValidation(unittest.TestCase):
    """Validate quiz data structure for all lessons."""

    def test_all_quiz_data_is_valid(self):
        """Verify all lessons with quizzes have valid question data."""
        for lesson_id, lesson_data in LESSONS.items():
            with self.subTest(lesson=lesson_id):
                if 'quiz' not in lesson_data:
                    continue  # Skip lessons without quizzes

                quiz_data = lesson_data['quiz']
                self.assertIsInstance(quiz_data, list,
                    f"{lesson_id}: quiz must be a list")
                self.assertGreater(len(quiz_data), 0,
                    f"{lesson_id}: quiz must have at least one question")

                # Validate each question
                for i, question in enumerate(quiz_data):
                    with self.subTest(lesson=lesson_id, question=i):
                        self._validate_question_structure(question, lesson_id, i)

    def _validate_question_structure(self, question, lesson_id, index):
        """Validate individual question structure."""
        # Required fields for all question types
        self.assertIn('type', question,
            f"{lesson_id} Q{index}: missing 'type'")
        self.assertIn('question', question,
            f"{lesson_id} Q{index}: missing 'question'")
        self.assertIn('explanation', question,
            f"{lesson_id} Q{index}: missing 'explanation'")

        q_type = question['type']

        # Type-specific validation
        if q_type == 'multiple_choice':
            self.assertIn('options', question,
                f"{lesson_id} Q{index}: multiple_choice missing 'options'")
            self.assertIn('correct', question,
                f"{lesson_id} Q{index}: multiple_choice missing 'correct'")
            self.assertIsInstance(question['options'], list,
                f"{lesson_id} Q{index}: options must be a list")
            self.assertGreaterEqual(len(question['options']), 2,
                f"{lesson_id} Q{index}: must have at least 2 options")
            self.assertLess(question['correct'], len(question['options']),
                f"{lesson_id} Q{index}: correct index out of range")

        elif q_type == 'true_false':
            self.assertIn('answer', question,
                f"{lesson_id} Q{index}: true_false missing 'answer'")
            self.assertIsInstance(question['answer'], bool,
                f"{lesson_id} Q{index}: answer must be boolean")

        elif q_type in ['command_recall', 'fill_blank']:
            self.assertIn('answer', question,
                f"{lesson_id} Q{index}: {q_type} missing 'answer'")
            self.assertIsInstance(question['answer'], str,
                f"{lesson_id} Q{index}: answer must be string")
            # Alternatives are optional
            if 'alternatives' in question:
                self.assertIsInstance(question['alternatives'], list,
                    f"{lesson_id} Q{index}: alternatives must be list")

    def test_quiz_question_counts(self):
        """Verify all quizzes have reasonable number of questions."""
        for lesson_id, lesson_data in LESSONS.items():
            if 'quiz' not in lesson_data:
                continue

            quiz_data = lesson_data['quiz']
            count = len(quiz_data)

            # Reasonable bounds: 5-15 questions per quiz
            self.assertGreaterEqual(count, 5,
                f"{lesson_id}: should have at least 5 questions (has {count})")
            self.assertLessEqual(count, 15,
                f"{lesson_id}: should have at most 15 questions (has {count})")

    def test_quiz_question_type_variety(self):
        """Ensure quizzes have diverse question types."""
        for lesson_id, lesson_data in LESSONS.items():
            if 'quiz' not in lesson_data:
                continue

            quiz_data = lesson_data['quiz']
            types = set(q['type'] for q in quiz_data)

            # Should have at least 2 different question types
            self.assertGreaterEqual(len(types), 2,
                f"{lesson_id}: quiz should use multiple question types")


class TestLessonQuizIntegration(unittest.TestCase):
    """Test quiz integration with lesson completion flow."""

    def setUp(self):
        """Set up test environment with temporary progress file."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_dir = Path(self.temp_dir)
        self.tutor = LinuxTutor()
        self.tutor.config_dir = self.config_dir
        self.tutor.progress_mgr = ProgressManager(self.config_dir)
        self.tutor.progress = self.tutor.progress_mgr.load_progress()

    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_lesson_not_marked_complete_when_quiz_declined(self, mock_stdout, mock_input):
        """Verify lesson isn't completed if user declines quiz."""
        # Inputs: skip exercise prompts, then decline quiz
        inputs = []
        inputs.append('')  # Press Enter to continue after explanation
        # Skip all exercise commands
        for _ in range(4):  # intro-to-terminal has 4 commands
            inputs.append('s')  # Skip
        inputs.append('n')  # Decline quiz

        mock_input.side_effect = inputs

        lesson = LESSONS['intro-to-terminal']
        initial_completed = len(self.tutor.progress['completed_lessons'])

        run_lesson(lesson, self.tutor)

        # Lesson should NOT be marked complete
        self.assertEqual(len(self.tutor.progress['completed_lessons']), initial_completed)
        self.assertNotIn('intro-to-terminal', self.tutor.progress['completed_lessons'])

    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_lesson_not_marked_complete_when_quiz_abandoned(self, mock_stdout, mock_input):
        """Verify lesson isn't completed if user quits quiz mid-way."""
        # Inputs: skip exercises, accept quiz, then quit after wrong answer
        inputs = []
        inputs.append('')  # Press Enter after explanation
        for _ in range(4):  # Skip 4 exercise commands
            inputs.append('s')
        inputs.append('y')  # Accept quiz
        inputs.append('wrong_answer')  # Wrong answer to Q1
        inputs.append('n')  # Decline retry

        mock_input.side_effect = inputs

        lesson = LESSONS['intro-to-terminal']
        initial_completed = len(self.tutor.progress['completed_lessons'])

        run_lesson(lesson, self.tutor)

        # Lesson should NOT be marked complete
        self.assertEqual(len(self.tutor.progress['completed_lessons']), initial_completed)
        self.assertNotIn('intro-to-terminal', self.tutor.progress['completed_lessons'])

    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_lesson_marked_complete_when_quiz_passed(self, mock_stdout, mock_input):
        """Verify lesson is completed when quiz is passed."""
        # Simulate completing intro-to-terminal lesson and quiz
        inputs = []
        inputs.append('')  # Press Enter after explanation
        # Skip 4 exercise commands
        for _ in range(4):
            inputs.append('s')
        inputs.append('y')  # Accept quiz
        # Provide correct answers for all 10 questions (each needs answer + enter to continue)
        inputs.extend(['a', ''])  # Q1: multiple choice + enter to continue
        inputs.extend(['whoami', ''])  # Q2: command recall + enter
        inputs.extend(['pwd', ''])  # Q3: command recall + enter
        inputs.extend(['false', ''])  # Q4: true/false + enter
        inputs.extend(['a', ''])  # Q5: multiple choice + enter
        inputs.extend(['date', ''])  # Q6: command recall + enter
        inputs.extend(['a', ''])  # Q7: multiple choice + enter
        inputs.extend(['true', ''])  # Q8: true/false + enter
        inputs.extend(['a', ''])  # Q9: multiple choice + enter
        inputs.extend(['true', ''])  # Q10: true/false + enter

        mock_input.side_effect = inputs

        lesson = LESSONS['intro-to-terminal']
        run_lesson(lesson, self.tutor)

        # Lesson should be marked complete
        self.assertIn('intro-to-terminal', self.tutor.progress['completed_lessons'])
        self.assertEqual(self.tutor.progress['stats']['quizzes_completed'], 1)
        self.assertEqual(self.tutor.progress['stats']['quiz_total_attempts'], 10)


class TestProgressManagerQuizIntegration(unittest.TestCase):
    """Test progress manager integration with quiz statistics."""

    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_dir = Path(self.temp_dir)
        self.progress_mgr = ProgressManager(self.config_dir)

    def test_increment_quiz_stats(self):
        """Test incrementing quiz statistics."""
        progress = self.progress_mgr.load_progress()

        # Initial state
        self.assertEqual(progress['stats']['quizzes_completed'], 0)
        self.assertEqual(progress['stats']['quiz_total_attempts'], 0)

        # Increment after completing quiz
        progress = self.progress_mgr.increment_quiz_stats(progress, 12)

        self.assertEqual(progress['stats']['quizzes_completed'], 1)
        self.assertEqual(progress['stats']['quiz_total_attempts'], 12)

        # Increment again
        progress = self.progress_mgr.increment_quiz_stats(progress, 8)

        self.assertEqual(progress['stats']['quizzes_completed'], 2)
        self.assertEqual(progress['stats']['quiz_total_attempts'], 20)

    def test_backward_compatibility_missing_quiz_stats(self):
        """Test loading old progress files without quiz stats."""
        # Create old-style progress file without quiz stats
        old_progress = {
            'first_time': False,
            'current_level': 'beginner',
            'current_lesson': None,
            'completed_lessons': ['intro-to-terminal'],
            'stats': {
                'lessons_completed': 1,
                'exercises_completed': 5
                # Missing: quizzes_completed, quiz_total_attempts
            }
        }

        # Write old progress file
        progress_file = self.config_dir / 'progress.json'
        self.config_dir.mkdir(parents=True, exist_ok=True)
        with open(progress_file, 'w') as f:
            json.dump(old_progress, f)

        # Load should add missing fields
        progress = self.progress_mgr.load_progress()

        self.assertIn('quizzes_completed', progress['stats'])
        self.assertIn('quiz_total_attempts', progress['stats'])
        self.assertEqual(progress['stats']['quizzes_completed'], 0)
        self.assertEqual(progress['stats']['quiz_total_attempts'], 0)

        # Old data should be preserved
        self.assertEqual(progress['current_level'], 'beginner')
        self.assertEqual(progress['stats']['lessons_completed'], 1)
        self.assertEqual(progress['stats']['exercises_completed'], 5)


class TestQuizCreation(unittest.TestCase):
    """Test Quiz object creation from lesson data."""

    def test_create_quiz_from_lesson_data(self):
        """Test creating Quiz from actual lesson quiz data."""
        for lesson_id, lesson_data in LESSONS.items():
            if 'quiz' not in lesson_data:
                continue

            with self.subTest(lesson=lesson_id):
                # Should not raise any exceptions
                quiz = Quiz(lesson_data['quiz'])
                self.assertEqual(len(quiz.questions), len(lesson_data['quiz']))

    def test_quiz_runner_with_all_lessons(self):
        """Test QuizRunner can be created for all lesson quizzes."""
        for lesson_id, lesson_data in LESSONS.items():
            if 'quiz' not in lesson_data:
                continue

            with self.subTest(lesson=lesson_id):
                quiz = Quiz(lesson_data['quiz'])
                runner = QuizRunner(quiz)
                self.assertIsNotNone(runner)
                self.assertEqual(runner.quiz, quiz)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""

    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_quiz_handles_interrupt(self, mock_stdout, mock_input):
        """Test quiz handles keyboard interrupt gracefully."""
        mock_input.side_effect = KeyboardInterrupt()

        lesson = LESSONS['intro-to-terminal']
        quiz = Quiz(lesson['quiz'])
        runner = QuizRunner(quiz)

        # Should not raise, should return incomplete
        attempts, completed = runner.run()
        self.assertFalse(completed)
        self.assertGreaterEqual(attempts, 1)

    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_quiz_handles_eof(self, mock_stdout, mock_input):
        """Test quiz handles EOF (Ctrl+D) gracefully."""
        mock_input.side_effect = EOFError()

        lesson = LESSONS['intro-to-terminal']
        quiz = Quiz(lesson['quiz'])
        runner = QuizRunner(quiz)

        # Should not raise, should return incomplete
        attempts, completed = runner.run()
        self.assertFalse(completed)
        self.assertGreaterEqual(attempts, 1)


if __name__ == '__main__':
    unittest.main()
