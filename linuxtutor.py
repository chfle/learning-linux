#!/usr/bin/env python3
"""
LinuxTutor - Interactive Linux Learning Platform

A modular, well-architected CLI tool for learning Linux from beginner to expert.
Uses clean separation of concerns with dedicated modules for UI, business logic, and data.
"""

import sys
import argparse
from pathlib import Path
from typing import Optional

# Core modules
from progress_manager import ProgressManager
from lesson_selector import (
    get_next_available_lesson,
    get_lessons_by_level,
    check_prerequisites,
    find_similar_lessons,
    get_blocked_lessons_info,
    are_all_lessons_completed
)

# UI modules  
from ui_display import (
    display_welcome_message,
    display_lesson_list,
    display_lesson_header,
    display_prerequisites_error,
    display_lesson_not_found,
    display_lesson_suggestions,
    display_help_text,
    display_status,
    display_post_lesson_menu,
    display_no_lessons_available,
    display_level_up_prompt,
    display_all_levels_completed,
    display_lesson_completion,
    display_starting_lesson,
    display_continuing_lesson,
    display_exit_message,
    display_generic_options,
    display_search_results
)

from ui_prompts import (
    prompt_yes_no,
    prompt_choice,
    prompt_lesson_selection,
    prompt_press_enter
)

# Constants
from constants import (
    VALID_LEVELS,
    LEVEL_BEGINNER,
    CONFIG_DIR_NAME,
    SEPARATOR_MEDIUM,
    AFFIRMATIVE_RESPONSES
)


class LinuxTutor:
    """Main application class - orchestrates learning experience."""

    def __init__(self):
        """Initialize the LinuxTutor application."""
        self.config_dir = Path.home() / CONFIG_DIR_NAME
        self.progress_mgr = ProgressManager(self.config_dir)
        self.progress = self.progress_mgr.load_progress()

    def save_progress(self) -> None:
        """Save current progress to disk."""
        self.progress_mgr.save_progress(self.progress)

    def list_lessons(self, level: Optional[str] = None) -> None:
        """
        List all lessons, optionally filtered by level.

        Args:
            level: Optional level to filter by
        """
        from lessons import LESSONS

        if level and level not in VALID_LEVELS:
            print(f"Invalid level. Choose from: {', '.join(VALID_LEVELS)}")
            return

        target_level = level if level else self.progress['current_level']
        lesson_ids = get_lessons_by_level(LESSONS, target_level)

        if not lesson_ids:
            print(f"\nNo lessons available for {target_level} level yet.")
            return

        completed = set(self.progress['completed_lessons'])
        display_lesson_list(lesson_ids, target_level, completed)

    def start_lesson(self, lesson_name: str) -> None:
        """
        Start a lesson (shows description only).

        Args:
            lesson_name: Lesson ID to start
        """
        from lessons import get_lesson

        lesson = get_lesson(lesson_name)
        if not lesson:
            self.show_lesson_not_found_help_original(lesson_name)
            return

        # Check prerequisites
        completed = set(self.progress['completed_lessons'])
        prereqs_met, missing = check_prerequisites(lesson, completed)

        if not prereqs_met:
            display_prerequisites_error(lesson_name, missing)
            return

        # Update progress
        self.progress = self.progress_mgr.set_current_lesson(self.progress, lesson_name)
        self.save_progress()

        # Display lesson info
        display_lesson_header(
            lesson['title'],
            lesson['level'],
            lesson['duration'],
            lesson['description']
        )

        if lesson.get('prerequisites'):
            print(f"\nPrerequisites: {', '.join(lesson['prerequisites'])}")

        print(f"\nTo continue with this lesson, run:")
        print(f"  linuxtutor lesson {lesson_name} --continue")

    def continue_lesson(self, lesson_name: str) -> None:
        """
        Continue/run a lesson interactively.

        Args:
            lesson_name: Lesson ID to continue
        """
        from lessons import get_lesson, run_lesson

        lesson = get_lesson(lesson_name)
        if not lesson:
            self.show_lesson_not_found_help_original(lesson_name)
            return

        # Check prerequisites
        completed = set(self.progress['completed_lessons'])
        prereqs_met, missing = check_prerequisites(lesson, completed)

        if not prereqs_met:
            display_prerequisites_error(lesson_name, missing)
            return

        # Run the lesson
        run_lesson(lesson, self)

        # After lesson completes, show post-lesson options
        self.show_post_lesson_options(lesson_name)

    def complete_lesson(self, lesson_name: str) -> None:
        """
        Mark a lesson as completed.

        Args:
            lesson_name: Lesson ID to mark complete
        """
        self.progress = self.progress_mgr.mark_lesson_complete(self.progress, lesson_name)
        self.save_progress()
        display_lesson_completion(lesson_name)

    def set_level(self, level: str) -> None:
        """
        Set user's current skill level.

        Args:
            level: Level to set
        """
        if level not in VALID_LEVELS:
            print(f"Invalid level. Choose from: {', '.join(VALID_LEVELS)}")
            return

        self.progress = self.progress_mgr.set_level(self.progress, level)
        self.save_progress()
        print(f"Level set to: {level}")

    def search_lessons(self, keywords: list, level_filter: Optional[str] = None) -> None:
        """
        Search for lessons matching keywords.

        Args:
            keywords: List of search terms
            level_filter: Optional level filter
        """
        from lessons import search_lessons as search_fn

        if not keywords:
            print("Error: Please provide at least one keyword to search for.")
            print("Usage: linuxtutor search <keyword> [<keyword2> ...]")
            return

        results = search_fn(keywords)

        if level_filter:
            results = [r for r in results if r['lesson_data']['level'] == level_filter]

        if not results:
            print(f"\nNo lessons found matching: {', '.join(keywords)}")
            print("\nTry:")
            print("  - Using fewer or different keywords")
            if level_filter:
                print("  - Searching without --level filter")
            print("  - Running 'linuxtutor lessons' to browse all lessons")
            return

        display_search_results(results, keywords)
        print(f"\nTo start a lesson, run: linuxtutor lesson <lesson-name>")

    def show_status(self) -> None:
        """Display user's progress and statistics."""
        display_status(self.progress)

    def show_help(self) -> None:
        """Display help information."""
        display_help_text()

    def start_learning(self) -> None:
        """Smart start command for new and returning users."""
        is_first_time = self.progress.get('first_time', True)

        if is_first_time:
            self.show_welcome()
        else:
            self.show_continue_options()

    # === Private Helper Methods ===

    def show_welcome(self) -> None:
        """Welcome flow for first-time users."""
        display_welcome_message(True, str(self.config_dir))

        # Mark as not first time since they've been welcomed
        self.progress = self.progress_mgr.mark_not_first_time(self.progress)
        self.save_progress()

        if not prompt_yes_no("\nReady to start your first lesson? [Y/n]: "):
            print("\nNo problem! When you're ready, run:")
            print("  linuxtutor start")
            display_generic_options()
            return

        display_starting_lesson("the basics")
        self.continue_lesson('intro-to-terminal')

    def show_continue_options(self) -> None:
        """Smart continuation for returning users."""
        from lessons import LESSONS

        current_lesson = self.progress.get('current_lesson')
        completed_count = len(self.progress['completed_lessons'])
        level = self.progress['current_level']

        display_welcome_message(False, str(self.config_dir))

        # Option 1: Continue ongoing lesson
        if current_lesson:
            print(f"You have an ongoing lesson: {current_lesson.replace('-', ' ').title()}")
            if prompt_yes_no("Continue this lesson? [Y/n]: "):
                self.continue_lesson(current_lesson)
                return

        # Option 2: No lessons completed yet
        if completed_count == 0:
            print("You haven't completed any lessons yet.")
            if prompt_yes_no("Start with the basics? [Y/n]: "):
                display_starting_lesson("the basics")
                self.continue_lesson('intro-to-terminal')
            else:
                display_generic_options()
            return

        # Option 3: Has completed lessons
        print(f"Progress: {completed_count} lessons completed ({level} level)")

        next_lesson = get_next_available_lesson(
            LESSONS,
            level,
            set(self.progress['completed_lessons'])
        )

        if next_lesson:
            next_title = LESSONS[next_lesson]['title']
            print(f"Suggested next lesson: {next_title}")

            if prompt_yes_no("Start this lesson? [Y/n]: "):
                display_continuing_lesson(next_title)
                self.continue_lesson(next_lesson)
            else:
                print("\nOther options:")
                print("  linuxtutor lessons    # see all lessons")
                print("  linuxtutor status     # check your progress")
        else:
            self.handle_no_available_lessons()

    def show_post_lesson_options(self, completed_lesson: str) -> None:
        """Show interactive menu after completing a lesson."""
        from lessons import LESSONS

        next_lesson = get_next_available_lesson(
            LESSONS,
            self.progress['current_level'],
            set(self.progress['completed_lessons'])
        )

        if next_lesson:
            next_title = LESSONS[next_lesson]['title']
            display_post_lesson_menu(True, next_title)

            choice = prompt_choice("\nYour choice [1-4]: ")

            if choice == '1' or choice == '':
                display_continuing_lesson(next_title)
                self.continue_lesson(next_lesson)
            elif choice == '2':
                self.list_lessons(self.progress['current_level'])
                lesson_id = prompt_lesson_selection()
                if lesson_id and lesson_id != 'exit':
                    self.continue_lesson(lesson_id)
            elif choice == '3':
                self.show_status()
                prompt_press_enter()
                self.show_post_lesson_options(completed_lesson)
            elif choice == '4':
                display_exit_message()
            else:
                print("Invalid choice. Exiting.")
        else:
            self.handle_no_available_lessons()

    def handle_no_available_lessons(self) -> None:
        """Handle when no lessons are available at current level."""
        from lessons import LESSONS

        current_level = self.progress['current_level']
        completed = set(self.progress['completed_lessons'])

        if are_all_lessons_completed(LESSONS, current_level, completed):
            print("Congratulations! You've completed all lessons in your current level.")
            self.suggest_level_up()
        else:
            blocked_lessons = get_blocked_lessons_info(LESSONS, current_level, completed)
            display_no_lessons_available(blocked_lessons, current_level)

            if prompt_yes_no("\nGo back to beginner level? [Y/n]: "):
                self.set_level(LEVEL_BEGINNER)
                print("\nRun 'linuxtutor start' to continue learning")

    def suggest_level_up(self) -> None:
        """Suggest moving to next level."""
        from lessons import LESSONS

        level_progression = VALID_LEVELS
        current_level = self.progress['current_level']

        try:
            current_index = level_progression.index(current_level)
            if current_index < len(level_progression) - 1:
                next_level = level_progression[current_index + 1]
                display_level_up_prompt(next_level)

                if prompt_yes_no("Move to next level? [Y/n]: "):
                    self.set_level(next_level)
                    next_lesson = get_next_available_lesson(
                        LESSONS,
                        next_level,
                        set(self.progress['completed_lessons'])
                    )
                    if next_lesson:
                        print(f"\nStarting your first {next_level} lesson!")
                        print(SEPARATOR_MEDIUM)
                        self.continue_lesson(next_lesson)
            else:
                display_all_levels_completed()
        except ValueError:
            pass

    def show_lesson_not_found_help_original(self, lesson_name: str) -> None:
        """Show helpful error when lesson doesn't exist."""
        from lessons import LESSONS, search_lessons

        display_lesson_not_found(lesson_name)

        # Try fuzzy search
        similar = find_similar_lessons(lesson_name, LESSONS)
        display_lesson_suggestions(similar)

        # Search by keywords
        keywords = lesson_name.split('-')
        results = search_lessons(keywords)
        if results:
            print("Lessons matching your search:")
            for i, result in enumerate(results[:3], 1):
                lesson = result['lesson_data']
                print(f"  {i}. {lesson['title']} ({lesson['level']})")
            print()

        print("Try:")
        print("  linuxtutor lessons           # Browse all available lessons")
        print(f"  linuxtutor search {lesson_name}   # Search for related lessons")
        print("  linuxtutor lessons beginner  # Start with beginner lessons")

    # === Backward Compatibility Methods for Tests ===

    def get_next_lesson(self):
        """Get next available lesson (wrapper for backward compatibility)."""
        from lessons import LESSONS
        return get_next_available_lesson(
            LESSONS,
            self.progress['current_level'],
            set(self.progress['completed_lessons'])
        )

    def check_prerequisites(self, lesson_data, lesson_name):
        """Check prerequisites (wrapper for backward compatibility)."""
        completed = set(self.progress['completed_lessons'])
        prereqs_met, missing = check_prerequisites(lesson_data, completed)
        if not prereqs_met:
            display_prerequisites_error(lesson_name, missing)
        return prereqs_met

    def show_lesson_not_found_help(self, lesson_name):
        """Show lesson not found help (wrapper for backward compatibility)."""
        self.show_lesson_not_found_help_original(lesson_name)


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description='LinuxTutor - Interactive Linux Learning',
        add_help=False
    )

    parser.add_argument('command', nargs='?', help='Command to execute')
    parser.add_argument('args', nargs='*', help='Command arguments')
    parser.add_argument('--continue', dest='continue_lesson', action='store_true',
                       help='Continue a lesson interactively')
    parser.add_argument('--level', '-l', dest='level_filter',
                       help='Filter by skill level')

    args = parser.parse_args()
    tutor = LinuxTutor()

    # No command - show smart welcome
    if len(sys.argv) == 1:
        is_first_time = tutor.progress.get('first_time', True)
        if is_first_time:
            print("Welcome to LinuxTutor!")
            print("To get started, run: linuxtutor start")
        else:
            print("LinuxTutor - Interactive Linux Learning")
            print("Run 'linuxtutor start' to continue learning or 'linuxtutor help' for options.")
        return

    # Execute command
    if args.command == 'start':
        tutor.start_learning()
    elif args.command == 'status':
        tutor.show_status()
    elif args.command == 'lessons':
        level = args.args[0] if args.args else None
        tutor.list_lessons(level)
    elif args.command == 'lesson':
        if not args.args:
            print("Error: Lesson name required")
            print("Usage: linuxtutor lesson <lesson-name>")
        else:
            lesson_name = args.args[0]
            if args.continue_lesson:
                tutor.continue_lesson(lesson_name)
            else:
                tutor.start_lesson(lesson_name)
    elif args.command == 'level':
        if not args.args:
            print(f"Current level: {tutor.progress['current_level']}")
        else:
            tutor.set_level(args.args[0])
    elif args.command == 'search':
        if not args.args:
            print("Error: Keywords required")
            print("Usage: linuxtutor search <keyword> [<keyword2> ...]")
        else:
            tutor.search_lessons(args.args, args.level_filter)
    elif args.command == 'help' or args.command == '--help':
        tutor.show_help()
    else:
        print(f"Unknown command: {args.command}")
        print("Run 'linuxtutor help' for usage information")


if __name__ == '__main__':
    main()
