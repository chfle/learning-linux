"""Quiz system for LinuxTutor lessons."""

from typing import Dict, Any, List
from constants import QUIZ_CHECKMARK, QUIZ_CROSSMARK, QUIZ_SEPARATOR


class QuizQuestion:
    """Base class for quiz questions."""

    def __init__(self, data: Dict[str, Any]):
        """
        Initialize quiz question.

        Args:
            data: Question data dictionary

        Raises:
            ValueError: If required keys are missing from data
        """
        if 'question' not in data:
            raise ValueError("Question data must contain 'question' key")
        if 'explanation' not in data:
            raise ValueError("Question data must contain 'explanation' key")

        self.question_text = data['question']
        self.explanation = data['explanation']

    def validate_answer(self, user_input: str) -> bool:
        """
        Validate user's answer.

        Args:
            user_input: User's answer

        Returns:
            True if correct, False otherwise

        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        raise NotImplementedError("Subclasses must implement validate_answer()")

    def display(self) -> None:
        """
        Display the question.

        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        raise NotImplementedError("Subclasses must implement display()")

    def get_explanation(self) -> str:
        """Get the explanation for this question."""
        return self.explanation


class MultipleChoiceQuestion(QuizQuestion):
    """Multiple choice question with A/B/C/D options."""

    def __init__(self, data: Dict[str, Any]):
        """
        Initialize multiple choice question.

        Args:
            data: Question data dictionary

        Raises:
            ValueError: If required keys are missing
        """
        super().__init__(data)
        if 'options' not in data:
            raise ValueError("MultipleChoiceQuestion requires 'options' key")
        if 'correct' not in data:
            raise ValueError("MultipleChoiceQuestion requires 'correct' key")

        self.options = data['options']
        self.correct_index = data['correct']

    def validate_answer(self, user_input: str) -> bool:
        """
        Validate user's answer.

        Accepts: A/B/C/D (case-insensitive) or 0/1/2/3

        Args:
            user_input: User's answer

        Returns:
            True if correct, False otherwise
        """
        user_input = user_input.strip().lower()

        # Check if it's a letter (a/b/c/d)
        if user_input in ['a', 'b', 'c', 'd']:
            letter_index = ord(user_input) - ord('a')
            if letter_index >= len(self.options):  # Add this check
                return False
            return letter_index == self.correct_index

        # Check if it's a number (0/1/2/3)
        if user_input.isdigit():
            idx = int(user_input)
            if idx >= len(self.options):  # Add this check
                return False
            return idx == self.correct_index

        return False

    def display(self) -> None:
        """Display the question with options."""
        print(self.question_text)
        print()
        for i, option in enumerate(self.options):
            letter = chr(ord('A') + i)
            print(f"{letter}) {option}")


class TrueFalseQuestion(QuizQuestion):
    """True/False question."""

    def __init__(self, data: Dict[str, Any]):
        """
        Initialize true/false question.

        Args:
            data: Question data dictionary

        Raises:
            ValueError: If required keys are missing
        """
        super().__init__(data)
        if 'answer' not in data:
            raise ValueError("TrueFalseQuestion requires 'answer' key")

        self.correct_answer = data['answer']

    def validate_answer(self, user_input: str) -> bool:
        """
        Validate user's answer.

        Accepts: true/false, t/f, yes/no, y/n, 1/0 (all case-insensitive)

        Args:
            user_input: User's answer

        Returns:
            True if correct, False otherwise
        """
        user_input = user_input.strip().lower()

        # Map inputs to boolean values
        true_inputs = ['true', 't', 'yes', 'y', '1']
        false_inputs = ['false', 'f', 'no', 'n', '0']

        if user_input in true_inputs:
            return self.correct_answer is True
        elif user_input in false_inputs:
            return self.correct_answer is False
        else:
            return False

    def display(self) -> None:
        """Display the question."""
        print(self.question_text)
        print("\n[True/False]")


class TextAnswerQuestion(QuizQuestion):
    """Base class for questions with text answers and alternatives."""

    def __init__(self, data: Dict[str, Any]):
        """Initialize text answer question."""
        super().__init__(data)
        if 'answer' not in data:
            raise ValueError(f"{self.__class__.__name__} must contain 'answer' key")
        self.correct_answer = data['answer']
        self.alternatives = data.get('alternatives', [])

    def validate_answer(self, user_input: str) -> bool:
        """
        Validate user's answer.

        Strips whitespace and checks against answer and alternatives.

        Args:
            user_input: User's answer

        Returns:
            True if correct, False otherwise
        """
        user_input = user_input.strip()

        # Check exact answer
        if user_input == self.correct_answer:
            return True

        # Check alternatives
        if user_input in self.alternatives:
            return True

        return False


class CommandRecallQuestion(TextAnswerQuestion):
    """Question asking user to recall a specific command."""

    def display(self) -> None:
        """Display the question."""
        print(self.question_text)
        print("\n[Type the command]")


class FillBlankQuestion(TextAnswerQuestion):
    """Fill in the blank question."""

    def display(self) -> None:
        """Display the question."""
        print(self.question_text)
        print("\n[Fill in the blank]")


class Quiz:
    """Quiz containing multiple questions."""

    # Map question types to classes
    QUESTION_TYPES = {
        'multiple_choice': MultipleChoiceQuestion,
        'true_false': TrueFalseQuestion,
        'command_recall': CommandRecallQuestion,
        'fill_blank': FillBlankQuestion,
    }

    def __init__(self, quiz_data: List[Dict[str, Any]]):
        """
        Initialize quiz with question data.

        Args:
            quiz_data: List of question dictionaries

        Raises:
            ValueError: If unknown question type encountered
        """
        self.questions = []
        for q_data in quiz_data:
            q_type = q_data.get('type')
            if q_type not in self.QUESTION_TYPES:
                raise ValueError(f"Unknown question type: {q_type}")

            question_class = self.QUESTION_TYPES[q_type]
            self.questions.append(question_class(q_data))


class QuizRunner:
    """Handles quiz presentation and user interaction."""

    def __init__(self, quiz: Quiz):
        """
        Initialize quiz runner.

        Args:
            quiz: Quiz instance to run
        """
        self.quiz = quiz

    def run(self) -> tuple:
        """
        Run the quiz interactively.

        Returns:
            Tuple of (total_attempts, completed) where completed is True if all questions answered
        """
        total_attempts = 0
        total_questions = len(self.quiz.questions)

        print("\n" + "━" * 42)
        print("Time to test your knowledge!")
        print("━" * 42)
        print(f"\nYou'll answer {total_questions} questions about what you just learned.")
        print("You can retake questions until you get them right.\n")

        try:
            for i, question in enumerate(self.quiz.questions, 1):
                while True:
                    total_attempts += 1

                    # Display question
                    print(f"\nQuestion {i} of {total_questions}")
                    print(QUIZ_SEPARATOR)
                    question.display()

                    # Get answer
                    user_answer = input("\nYour answer: ").strip()

                    # Validate
                    if question.validate_answer(user_answer):
                        print(f"\n{QUIZ_CHECKMARK} Correct!")
                        print(f"\nExplanation: {question.get_explanation()}")
                        input("\n[Press Enter to continue...]")
                        break
                    else:
                        print(f"\n{QUIZ_CROSSMARK} Incorrect.")
                        print(f"\nExplanation: {question.get_explanation()}")

                        retry = input("\nTry again? [Y/n]: ").strip().lower()
                        if retry not in ['', 'y', 'yes']:
                            # User chose not to retry - quiz incomplete
                            return (total_attempts, False)

            # All questions answered correctly
            self._show_completion(total_attempts, total_questions)
            return (total_attempts, True)

        except (EOFError, KeyboardInterrupt):
            # Handle Ctrl+D (EOF) or Ctrl+C gracefully
            print("\n\nQuiz interrupted.")
            print(f"You answered {i-1} out of {total_questions} questions.")
            return (total_attempts, False)

    def _show_completion(self, attempts: int, total: int) -> None:
        """Show quiz completion summary."""
        print("\n" + "━" * 42)
        print("Quiz Complete!")
        print("━" * 42)
        print(f"\nYou answered all {total} questions correctly!")

        retries = attempts - total
        if retries > 0:
            plural = 's' if retries > 1 else ''
            print(f"Total attempts: {attempts} ({retries} question{plural} needed retries)")
        else:
            print("Perfect score - all correct on first try!")

        print("\nGreat job!")
