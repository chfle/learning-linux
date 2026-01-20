"""User interface display functions - all print statements."""

from typing import List, Optional, Set
from constants import (
    SEPARATOR_LIGHT, SEPARATOR_MEDIUM, SEPARATOR_HEAVY,
    CHECKBOX_COMPLETED, CHECKBOX_PENDING
)


def display_welcome_message(first_time: bool, config_dir: str) -> None:
    """Display welcome message for first-time or returning users."""
    if first_time:
        print("Welcome to LinuxTutor!")
        print(SEPARATOR_MEDIUM)
        print("\nYou're about to start your Linux learning journey!")
        print("LinuxTutor will guide you from complete beginner to Linux expert.")
        print("\nHere's how it works:")
        print("- Progressive lessons from beginner to expert level")
        print("- Hands-on exercises with real commands")
        print("- Your progress is automatically saved")
        print("- Safe practice environment")
        print(f"\nYour progress will be saved in: {config_dir}")
    else:
        print("Welcome back to LinuxTutor!")
        print(SEPARATOR_LIGHT)


def display_lesson_list(lesson_ids: List[str], level: str, completed_lessons: Set[str]) -> None:
    """Display a formatted list of lessons."""
    print(f"\n{level.title()} Level Lessons:")
    for i, lesson_id in enumerate(lesson_ids, 1):
        status = CHECKBOX_COMPLETED if lesson_id in completed_lessons else CHECKBOX_PENDING
        title = lesson_id.replace('-', ' ').title()
        print(f"  {status} {i}. {title}")


def display_lesson_header(title: str, level: str, duration: int, description: str) -> None:
    """Display lesson header information."""
    print(f"\n=== {title} ===")
    print(f"Level: {level.title()}")
    print(f"Duration: ~{duration} minutes\n")
    print(description)


def display_prerequisites_error(lesson_name: str, missing_prereqs: List[str]) -> None:
    """Display error message for missing prerequisites."""
    print(f"\nWARNING: Cannot start '{lesson_name}' yet.")
    print("You need to complete these lessons first:")
    for prereq in missing_prereqs:
        print(f"  - {prereq.replace('-', ' ').title()}")
    print(f"\nStart with: linuxtutor lesson {missing_prereqs[0]}")


def display_lesson_not_found(lesson_name: str) -> None:
    """Display error message for lesson not found."""
    print(f"\nERROR: Lesson '{lesson_name}' not found.\n")


def display_lesson_suggestions(similar_lessons: List[str]) -> None:
    """Display suggested similar lessons."""
    if similar_lessons:
        print("Did you mean:")
        for lesson in similar_lessons:
            print(f"  - {lesson}")
        print()


def display_search_results(results: List[dict], keywords: List[str]) -> None:
    """Display search results with lesson details."""
    from lessons import LESSONS

    if not results:
        print(f"\nNo lessons found matching: {', '.join(keywords)}")
        return

    plural = 's' if len(results) != 1 else ''
    print(f"\nFound {len(results)} lesson{plural} matching: {', '.join(keywords)}\n")

    for i, result in enumerate(results, 1):
        lesson = result['lesson_data']
        print(f"{i}. [{lesson['level'].title()}] {lesson['title']} (Score: {result['score']})")
        print(f"   Duration: {lesson['duration']} minutes")


def display_help_text() -> None:
    """Display help information."""
    help_text = """
LinuxTutor - Interactive Linux Learning CLI

Commands:
  start              - Smart start: continue your learning journey
  status             - View your progress and statistics
  lessons [level]    - List available lessons (optionally filter by level)
  lesson <name>      - Start a specific lesson
  level <level>      - Set your current skill level
  search <keywords>  - Search lessons by keywords
  help               - Show this help message

Examples:
  linuxtutor start
  linuxtutor lessons beginner
  linuxtutor lesson intro-to-terminal
  linuxtutor search file permissions
  linuxtutor level intermediate

Skill Levels:
  beginner, intermediate, advanced, expert
"""
    print(help_text)


def display_status(progress: dict) -> None:
    """Display user's current progress and statistics."""
    print("\nYour Progress")
    print(SEPARATOR_LIGHT)
    print(f"Current Level: {progress['current_level'].title()}")
    print(f"Lessons Completed: {progress['stats']['lessons_completed']}")
    print(f"Exercises Completed: {progress['stats']['exercises_completed']}")

    if progress.get('current_lesson'):
        print(f"Current Lesson: {progress['current_lesson'].replace('-', ' ').title()}")

    if progress['completed_lessons']:
        print("\nCompleted Lessons:")
        for lesson in progress['completed_lessons']:
            print(f"  {CHECKBOX_COMPLETED} {lesson.replace('-', ' ').title()}")


def display_post_lesson_menu(has_next_lesson: bool, next_lesson_title: Optional[str] = None) -> None:
    """Display the post-lesson action menu."""
    print("\n" + SEPARATOR_MEDIUM)
    print("What would you like to do next?")
    print(SEPARATOR_MEDIUM)

    if has_next_lesson and next_lesson_title:
        print(f"\n1. Continue to next lesson: {next_lesson_title}")
        print("2. Choose a different lesson")
        print("3. View your progress")
        print("4. Exit")
    else:
        print("\n1. Level up to next difficulty")
        print("2. View your progress")
        print("3. Exit")


def display_no_lessons_available(blocked_lessons: List[tuple], current_level: str) -> None:
    """Display message when no lessons are available due to unmet prerequisites."""
    print("\nNo lessons available at your current level yet.")
    print("You need to complete prerequisite lessons first.")
    print()

    if blocked_lessons:
        print("Lessons blocked by prerequisites:")
        for lesson_title, missing_prereqs in blocked_lessons[:3]:
            print(f"  - {lesson_title}")
            prereq_titles = [p.replace('-', ' ').title() for p in missing_prereqs]
            print(f"    Need: {', '.join(prereq_titles)}")

    print()
    print("Recommendations:")
    print("1. Go back and complete beginner lessons")
    print(f"2. Run 'linuxtutor lessons beginner' to see available lessons")
    print("3. Run 'linuxtutor status' to check your progress")


def display_level_up_prompt(next_level: str) -> None:
    """Display level up prompt."""
    print(f"\nReady to level up to {next_level.title()}?")


def display_all_levels_completed() -> None:
    """Display message when user has completed all levels."""
    print("Amazing! You've mastered all Linux levels!")
    print("Consider contributing to the project or mentoring others!")


def display_lesson_completion(lesson_name: str) -> None:
    """Display lesson completion message."""
    print(f"[COMPLETED] Lesson: {lesson_name}")


def display_starting_lesson(lesson_title: str) -> None:
    """Display message when starting a lesson."""
    print("\nLet's begin!")
    print(SEPARATOR_MEDIUM)


def display_continuing_lesson(lesson_title: str) -> None:
    """Display message when continuing to a lesson."""
    print(f"\nStarting: {lesson_title}")
    print(SEPARATOR_MEDIUM)


def display_exit_message() -> None:
    """Display exit message."""
    print("\nGreat work! Come back anytime to continue learning.")
    print("Run 'linuxtutor start' to pick up where you left off.")


def display_generic_options() -> None:
    """Display generic options for continuing."""
    print("\nOther options:")
    print("  linuxtutor lessons    # see all lessons")
    print("  linuxtutor help       # for more options")
