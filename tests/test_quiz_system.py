#!/usr/bin/env python3

import unittest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
from io import StringIO

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from constants import QUIZ_CHECKMARK, QUIZ_CROSSMARK, QUIZ_SEPARATOR
from quiz_system import QuizQuestion, MultipleChoiceQuestion, TrueFalseQuestion, CommandRecallQuestion, FillBlankQuestion, Quiz, QuizRunner
from progress_manager import ProgressManager
import tempfile


class TestQuizConstants(unittest.TestCase):
    """Test quiz-related constants exist."""

    def test_quiz_display_constants_exist(self):
        """Test that quiz display constants are defined."""
        self.assertEqual(QUIZ_CHECKMARK, '✓')
        self.assertEqual(QUIZ_CROSSMARK, '✗')
        self.assertIsInstance(QUIZ_SEPARATOR, str)
        self.assertGreater(len(QUIZ_SEPARATOR), 0)


class TestQuizQuestionBase(unittest.TestCase):
    """Test QuizQuestion base class."""

    def test_quiz_question_has_required_attributes(self):
        """Test QuizQuestion stores question data."""
        data = {
            'type': 'test_type',
            'question': 'Test question?',
            'explanation': 'Test explanation'
        }
        q = QuizQuestion(data)
        self.assertEqual(q.question_text, 'Test question?')
        self.assertEqual(q.explanation, 'Test explanation')

    def test_quiz_question_validate_not_implemented(self):
        """Test QuizQuestion base validate_answer raises NotImplementedError."""
        data = {'question': 'Test?', 'explanation': 'Explanation'}
        q = QuizQuestion(data)
        with self.assertRaises(NotImplementedError):
            q.validate_answer('any input')

    def test_quiz_question_display_not_implemented(self):
        """Test QuizQuestion base display raises NotImplementedError."""
        data = {'question': 'Test?', 'explanation': 'Explanation'}
        q = QuizQuestion(data)
        with self.assertRaises(NotImplementedError):
            q.display()

    def test_quiz_question_missing_question_key(self):
        """Test QuizQuestion raises error when question key is missing."""
        data = {'explanation': 'Test explanation'}
        with self.assertRaises(ValueError):
            QuizQuestion(data)

    def test_quiz_question_missing_explanation_key(self):
        """Test QuizQuestion raises error when explanation key is missing."""
        data = {'question': 'Test question?'}
        with self.assertRaises(ValueError):
            QuizQuestion(data)

    def test_get_explanation_returns_explanation(self):
        """Test get_explanation returns the correct explanation."""
        data = {
            'question': 'Test question?',
            'explanation': 'This is the explanation'
        }
        q = QuizQuestion(data)
        self.assertEqual(q.get_explanation(), 'This is the explanation')


class TestMultipleChoiceQuestion(unittest.TestCase):
    """Test MultipleChoiceQuestion class."""

    def setUp(self):
        """Set up test data."""
        self.data = {
            'type': 'multiple_choice',
            'question': 'What does pwd do?',
            'options': ['Print Working Directory', 'Power Directory', 'Present Data', 'Process Dir'],
            'correct': 0,
            'explanation': 'pwd prints working directory'
        }
        self.question = MultipleChoiceQuestion(self.data)

    def test_accepts_letter_answers_case_insensitive(self):
        """Test accepts A/B/C/D in any case."""
        self.assertTrue(self.question.validate_answer('a'))
        self.assertTrue(self.question.validate_answer('A'))
        self.assertFalse(self.question.validate_answer('b'))
        self.assertFalse(self.question.validate_answer('B'))

    def test_accepts_numeric_index(self):
        """Test accepts 0/1/2/3 as index."""
        self.assertTrue(self.question.validate_answer('0'))
        self.assertFalse(self.question.validate_answer('1'))
        self.assertFalse(self.question.validate_answer('2'))

    def test_rejects_invalid_input(self):
        """Test rejects invalid choices."""
        self.assertFalse(self.question.validate_answer(''))
        self.assertFalse(self.question.validate_answer('e'))
        self.assertFalse(self.question.validate_answer('5'))
        self.assertFalse(self.question.validate_answer('xyz'))

    def test_stores_options_and_correct_answer(self):
        """Test stores all options and correct index."""
        self.assertEqual(len(self.question.options), 4)
        self.assertEqual(self.question.correct_index, 0)
        self.assertEqual(self.question.options[0], 'Print Working Directory')

    def test_missing_options_key(self):
        """Test raises error when options key is missing."""
        data = {
            'type': 'multiple_choice',
            'question': 'Test?',
            'correct': 0,
            'explanation': 'Test explanation'
        }
        with self.assertRaises(ValueError) as context:
            MultipleChoiceQuestion(data)
        self.assertIn('options', str(context.exception))

    def test_missing_correct_key(self):
        """Test raises error when correct key is missing."""
        data = {
            'type': 'multiple_choice',
            'question': 'Test?',
            'options': ['A', 'B'],
            'explanation': 'Test explanation'
        }
        with self.assertRaises(ValueError) as context:
            MultipleChoiceQuestion(data)
        self.assertIn('correct', str(context.exception))


class TestTrueFalseQuestion(unittest.TestCase):
    """Test TrueFalseQuestion class."""

    def setUp(self):
        """Set up test data."""
        self.data = {
            'type': 'true_false',
            'question': '/home contains config files.',
            'answer': False,
            'explanation': '/home contains user directories, /etc has config files'
        }
        self.question = TrueFalseQuestion(self.data)

    def test_accepts_true_false_words(self):
        """Test accepts true/false words case-insensitive."""
        true_data = {**self.data, 'answer': True}
        true_q = TrueFalseQuestion(true_data)

        self.assertTrue(true_q.validate_answer('true'))
        self.assertTrue(true_q.validate_answer('TRUE'))
        self.assertTrue(true_q.validate_answer('True'))
        self.assertFalse(true_q.validate_answer('false'))

    def test_accepts_t_f_letters(self):
        """Test accepts t/f letters."""
        self.assertTrue(self.question.validate_answer('f'))  # Correct - answer is False
        self.assertTrue(self.question.validate_answer('F'))  # Correct - answer is False
        self.assertFalse(self.question.validate_answer('t'))  # Wrong - answer is False

    def test_accepts_yes_no(self):
        """Test accepts yes/no."""
        false_q = self.question
        self.assertTrue(false_q.validate_answer('no'))  # Correct - answer is False
        self.assertTrue(false_q.validate_answer('NO'))  # Correct - answer is False
        self.assertFalse(false_q.validate_answer('yes'))  # Wrong - answer is False

    def test_accepts_y_n(self):
        """Test accepts y/n."""
        self.assertTrue(self.question.validate_answer('n'))  # Correct - answer is False
        self.assertFalse(self.question.validate_answer('y'))  # Wrong - answer is False

    def test_accepts_1_0(self):
        """Test accepts 1/0 for true/false."""
        self.assertTrue(self.question.validate_answer('0'))  # Correct - answer is False
        self.assertFalse(self.question.validate_answer('1'))  # Wrong - answer is False

    def test_rejects_invalid_input(self):
        """Test rejects invalid input."""
        self.assertFalse(self.question.validate_answer(''))
        self.assertFalse(self.question.validate_answer('maybe'))
        self.assertFalse(self.question.validate_answer('2'))

    def test_missing_answer_key(self):
        """Test raises error when answer key is missing."""
        data = {
            'type': 'true_false',
            'question': 'Test?',
            'explanation': 'Test explanation'
        }
        with self.assertRaises(ValueError) as context:
            TrueFalseQuestion(data)
        self.assertIn('answer', str(context.exception))


class TestCommandRecallQuestion(unittest.TestCase):
    """Test CommandRecallQuestion class."""

    def setUp(self):
        """Set up test data."""
        self.data = {
            'type': 'command_recall',
            'question': 'Which command shows your username?',
            'answer': 'whoami',
            'alternatives': ['id -un'],
            'explanation': 'whoami displays current username'
        }
        self.question = CommandRecallQuestion(self.data)

    def test_accepts_exact_answer(self):
        """Test accepts exact answer."""
        self.assertTrue(self.question.validate_answer('whoami'))

    def test_accepts_answer_with_whitespace(self):
        """Test strips whitespace from answer."""
        self.assertTrue(self.question.validate_answer('  whoami  '))
        self.assertTrue(self.question.validate_answer('whoami\n'))

    def test_accepts_alternatives(self):
        """Test accepts alternative correct answers."""
        self.assertTrue(self.question.validate_answer('id -un'))
        self.assertTrue(self.question.validate_answer('  id -un  '))

    def test_rejects_wrong_answer(self):
        """Test rejects wrong answers."""
        self.assertFalse(self.question.validate_answer(''))
        self.assertFalse(self.question.validate_answer('pwd'))
        self.assertFalse(self.question.validate_answer('who'))

    def test_handles_missing_alternatives(self):
        """Test works when alternatives field is missing."""
        data_no_alt = {
            'type': 'command_recall',
            'question': 'Test?',
            'answer': 'test',
            'explanation': 'Test explanation'
        }
        q = CommandRecallQuestion(data_no_alt)
        self.assertTrue(q.validate_answer('test'))
        self.assertFalse(q.validate_answer('other'))

    def test_missing_answer_key(self):
        """Test raises error when answer key is missing."""
        data = {
            'type': 'command_recall',
            'question': 'Test?',
            'explanation': 'Test explanation'
        }
        with self.assertRaises(ValueError) as context:
            CommandRecallQuestion(data)
        self.assertIn('answer', str(context.exception))


class TestFillBlankQuestion(unittest.TestCase):
    """Test FillBlankQuestion class."""

    def setUp(self):
        """Set up test data."""
        self.data = {
            'type': 'fill_blank',
            'question': 'To list all files including hidden: ls ____',
            'answer': '-a',
            'alternatives': ['-la', '-al', '--all'],
            'explanation': '-a shows all files including hidden'
        }
        self.question = FillBlankQuestion(self.data)

    def test_accepts_exact_answer(self):
        """Test accepts exact answer."""
        self.assertTrue(self.question.validate_answer('-a'))

    def test_accepts_alternatives(self):
        """Test accepts alternative answers."""
        self.assertTrue(self.question.validate_answer('-la'))
        self.assertTrue(self.question.validate_answer('-al'))
        self.assertTrue(self.question.validate_answer('--all'))

    def test_strips_whitespace(self):
        """Test strips whitespace from answer."""
        self.assertTrue(self.question.validate_answer('  -a  '))
        self.assertTrue(self.question.validate_answer('  -la  '))

    def test_rejects_wrong_answer(self):
        """Test rejects wrong answers."""
        self.assertFalse(self.question.validate_answer(''))
        self.assertFalse(self.question.validate_answer('-l'))
        self.assertFalse(self.question.validate_answer('ls'))

    def test_handles_missing_alternatives(self):
        """Test works when alternatives field is missing."""
        data_no_alt = {
            'type': 'fill_blank',
            'question': 'cd ____',
            'answer': '..',
            'explanation': 'cd .. goes up one directory'
        }
        q = FillBlankQuestion(data_no_alt)
        self.assertTrue(q.validate_answer('..'))
        self.assertFalse(q.validate_answer('/'))

    def test_missing_answer_key(self):
        """Test raises error when answer key is missing."""
        data = {
            'type': 'fill_blank',
            'question': 'Test ____?',
            'explanation': 'Test explanation'
        }
        with self.assertRaises(ValueError) as context:
            FillBlankQuestion(data)
        self.assertIn('answer', str(context.exception))


class TestQuiz(unittest.TestCase):
    """Test Quiz class."""

    def setUp(self):
        """Set up test quiz data."""
        self.quiz_data = [
            {
                'type': 'multiple_choice',
                'question': 'What is pwd?',
                'options': ['Print Working Directory', 'Other'],
                'correct': 0,
                'explanation': 'Explanation 1'
            },
            {
                'type': 'true_false',
                'question': '/home has configs?',
                'answer': False,
                'explanation': 'Explanation 2'
            }
        ]

    def test_quiz_initializes_questions(self):
        """Test Quiz creates question objects from data."""
        quiz = Quiz(self.quiz_data)
        self.assertEqual(len(quiz.questions), 2)
        self.assertIsInstance(quiz.questions[0], MultipleChoiceQuestion)
        self.assertIsInstance(quiz.questions[1], TrueFalseQuestion)

    def test_quiz_handles_empty_list(self):
        """Test Quiz handles empty question list."""
        quiz = Quiz([])
        self.assertEqual(len(quiz.questions), 0)

    def test_quiz_raises_on_unknown_type(self):
        """Test Quiz raises ValueError on unknown question type."""
        bad_data = [{'type': 'unknown_type', 'question': 'test?', 'explanation': 'test'}]
        with self.assertRaises(ValueError) as context:
            Quiz(bad_data)
        self.assertIn('Unknown question type', str(context.exception))


class TestQuizRunner(unittest.TestCase):
    """Test QuizRunner class."""

    def setUp(self):
        """Set up test quiz."""
        quiz_data = [
            {
                'type': 'multiple_choice',
                'question': 'What is pwd?',
                'options': ['Print Working Directory', 'Other', 'Wrong', 'Nope'],
                'correct': 0,
                'explanation': 'pwd is Print Working Directory'
            }
        ]
        self.quiz = Quiz(quiz_data)
        self.runner = QuizRunner(self.quiz)

    @patch('builtins.input', side_effect=['a', ''])
    @patch('sys.stdout', new_callable=StringIO)
    def test_run_quiz_correct_first_try(self, mock_stdout, mock_input):
        """Test running quiz with correct answer on first try."""
        attempts, completed = self.runner.run()
        self.assertEqual(attempts, 1)
        self.assertTrue(completed)
        output = mock_stdout.getvalue()
        self.assertIn('Quiz Complete!', output)
        self.assertIn('✓', output)

    @patch('builtins.input', side_effect=['b', 'n'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_run_quiz_wrong_answer_no_retry(self, mock_stdout, mock_input):
        """Test quiz can be exited on wrong answer."""
        attempts, completed = self.runner.run()
        self.assertEqual(attempts, 1)
        self.assertFalse(completed)
        output = mock_stdout.getvalue()
        self.assertIn('✗', output)

    @patch('builtins.input', side_effect=['b', 'y', 'a', ''])
    @patch('sys.stdout', new_callable=StringIO)
    def test_run_quiz_retry_until_correct(self, mock_stdout, mock_input):
        """Test quiz allows retries until correct."""
        attempts, completed = self.runner.run()
        self.assertEqual(attempts, 2)
        self.assertTrue(completed)
        output = mock_stdout.getvalue()
        self.assertIn('Quiz Complete!', output)

    @patch('builtins.input', side_effect=['a', '', 'f', ''])
    @patch('sys.stdout', new_callable=StringIO)
    def test_run_quiz_multiple_questions(self, mock_stdout, mock_input):
        """Test quiz with multiple questions."""
        quiz_data = [
            {
                'type': 'multiple_choice',
                'question': 'Question 1?',
                'options': ['Answer 1', 'Wrong'],
                'correct': 0,
                'explanation': 'Explanation 1'
            },
            {
                'type': 'true_false',
                'question': 'Question 2?',
                'answer': False,
                'explanation': 'Explanation 2'
            }
        ]
        quiz = Quiz(quiz_data)
        runner = QuizRunner(quiz)
        attempts, completed = runner.run()
        self.assertEqual(attempts, 2)
        self.assertTrue(completed)
        output = mock_stdout.getvalue()
        self.assertIn('Quiz Complete!', output)
        self.assertIn('Question 1 of 2', output)
        self.assertIn('Question 2 of 2', output)

    @patch('builtins.input', side_effect=['b', 'yes', 'c', 'y', 'a', ''])
    @patch('sys.stdout', new_callable=StringIO)
    def test_run_quiz_multiple_retries(self, mock_stdout, mock_input):
        """Test quiz with multiple retries on same question."""
        attempts, completed = self.runner.run()
        self.assertEqual(attempts, 3)
        self.assertTrue(completed)
        output = mock_stdout.getvalue()
        self.assertIn('Quiz Complete!', output)
        self.assertIn('2 questions needed retries', output)

    @patch('builtins.input', side_effect=['a', ''])
    @patch('sys.stdout', new_callable=StringIO)
    def test_run_quiz_perfect_score_message(self, mock_stdout, mock_input):
        """Test perfect score message displayed."""
        attempts, completed = self.runner.run()
        self.assertEqual(attempts, 1)
        self.assertTrue(completed)
        output = mock_stdout.getvalue()
        self.assertIn('Perfect score - all correct on first try!', output)

    @patch('builtins.input', side_effect=['b', 'y', 'a', ''])
    @patch('sys.stdout', new_callable=StringIO)
    def test_run_quiz_retry_message_singular(self, mock_stdout, mock_input):
        """Test retry message uses singular form for one retry."""
        attempts, completed = self.runner.run()
        self.assertEqual(attempts, 2)
        self.assertTrue(completed)
        output = mock_stdout.getvalue()
        self.assertIn('1 question needed retries', output)


class TestProgressManagerQuizStats(unittest.TestCase):
    """Test ProgressManager quiz statistics."""

    def setUp(self):
        """Set up test progress manager."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.progress_mgr = ProgressManager(self.temp_dir)

    def test_default_progress_has_quiz_stats(self):
        """Test default progress includes quiz stats."""
        progress = self.progress_mgr.load_progress()
        self.assertIn('quizzes_completed', progress['stats'])
        self.assertIn('quiz_total_attempts', progress['stats'])
        self.assertEqual(progress['stats']['quizzes_completed'], 0)
        self.assertEqual(progress['stats']['quiz_total_attempts'], 0)

    def test_increment_quiz_stats(self):
        """Test incrementing quiz statistics."""
        progress = self.progress_mgr.load_progress()
        progress = self.progress_mgr.increment_quiz_stats(progress, attempts=12)

        self.assertEqual(progress['stats']['quizzes_completed'], 1)
        self.assertEqual(progress['stats']['quiz_total_attempts'], 12)

        # Increment again
        progress = self.progress_mgr.increment_quiz_stats(progress, attempts=8)
        self.assertEqual(progress['stats']['quizzes_completed'], 2)
        self.assertEqual(progress['stats']['quiz_total_attempts'], 20)


if __name__ == '__main__':
    unittest.main()
