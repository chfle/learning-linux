"""User interface prompt functions - all input collection."""

from constants import AFFIRMATIVE_RESPONSES


def prompt_yes_no(message: str) -> bool:
    """
    Prompt user with a yes/no question.

    Args:
        message: The prompt message to display

    Returns:
        True if user answered affirmatively, False otherwise
    """
    response = input(message).lower().strip()
    return response in AFFIRMATIVE_RESPONSES


def prompt_choice(message: str) -> str:
    """
    Prompt user for a choice.

    Args:
        message: The prompt message to display

    Returns:
        User's choice as a string
    """
    return input(message).strip()


def prompt_lesson_selection() -> str:
    """
    Prompt user to select a lesson.

    Returns:
        Selected lesson name
    """
    return input("\nEnter lesson name (or 'exit' to quit): ").strip()


def prompt_press_enter(message: str = "\nPress Enter to continue...") -> None:
    """
    Prompt user to press Enter to continue.

    Args:
        message: Optional custom message
    """
    input(message)
