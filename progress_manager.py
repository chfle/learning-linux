"""Progress persistence and management."""

import json
from pathlib import Path
from typing import Dict, Any
from constants import (
    CONFIG_DIR_NAME,
    PROGRESS_FILE_NAME,
    DEFAULT_LEVEL,
    DEFAULT_FIRST_TIME
)


class ProgressManager:
    """Handles loading, saving, and updating user progress."""

    def __init__(self, config_dir: Path):
        """
        Initialize progress manager.

        Args:
            config_dir: Directory to store progress file
        """
        self.config_dir = config_dir
        self.progress_file = config_dir / PROGRESS_FILE_NAME

    def load_progress(self) -> Dict[str, Any]:
        """
        Load progress from file or create default progress.

        Returns:
            Progress dictionary
        """
        if self.progress_file.exists():
            with open(self.progress_file, 'r') as f:
                return json.load(f)

        return self._create_default_progress()

    def save_progress(self, progress: Dict[str, Any]) -> None:
        """
        Save progress to file.

        Args:
            progress: Progress dictionary to save
        """
        self.config_dir.mkdir(parents=True, exist_ok=True)

        with open(self.progress_file, 'w') as f:
            json.dump(progress, f, indent=2)

    def _create_default_progress(self) -> Dict[str, Any]:
        """
        Create default progress structure.

        Returns:
            Default progress dictionary
        """
        return {
            'first_time': DEFAULT_FIRST_TIME,
            'current_level': DEFAULT_LEVEL,
            'current_lesson': None,
            'completed_lessons': [],
            'stats': {
                'lessons_completed': 0,
                'exercises_completed': 0
            }
        }

    def mark_lesson_complete(self, progress: Dict[str, Any], lesson_name: str) -> Dict[str, Any]:
        """
        Mark a lesson as completed in progress.

        Args:
            progress: Current progress dictionary
            lesson_name: Lesson ID to mark as complete

        Returns:
            Updated progress dictionary
        """
        if lesson_name not in progress['completed_lessons']:
            progress['completed_lessons'].append(lesson_name)
            progress['stats']['lessons_completed'] += 1

        progress['current_lesson'] = None
        return progress

    def set_current_lesson(self, progress: Dict[str, Any], lesson_name: str) -> Dict[str, Any]:
        """
        Set the current lesson in progress.

        Args:
            progress: Current progress dictionary
            lesson_name: Lesson ID to set as current

        Returns:
            Updated progress dictionary
        """
        progress['current_lesson'] = lesson_name
        return progress

    def set_level(self, progress: Dict[str, Any], level: str) -> Dict[str, Any]:
        """
        Set user's current level.

        Args:
            progress: Current progress dictionary
            level: New level to set

        Returns:
            Updated progress dictionary
        """
        progress['current_level'] = level
        return progress

    def increment_exercises(self, progress: Dict[str, Any], count: int = 1) -> Dict[str, Any]:
        """
        Increment completed exercises count.

        Args:
            progress: Current progress dictionary
            count: Number of exercises to add

        Returns:
            Updated progress dictionary
        """
        progress['stats']['exercises_completed'] += count
        return progress

    def mark_not_first_time(self, progress: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mark that user is no longer first-time.

        Args:
            progress: Current progress dictionary

        Returns:
            Updated progress dictionary
        """
        progress['first_time'] = False
        return progress
