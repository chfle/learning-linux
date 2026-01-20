"""Lesson selection and filtering logic."""

from typing import Optional, List, Set, Tuple


def get_next_available_lesson(
    lessons_dict: dict,
    current_level: str,
    completed_lessons: Set[str]
) -> Optional[str]:
    """
    Find the next uncompleted lesson in current level with all prerequisites met.

    Args:
        lessons_dict: Dictionary of all lessons
        current_level: User's current level
        completed_lessons: Set of completed lesson IDs

    Returns:
        Lesson ID of next available lesson, or None if no lessons available
    """
    # Get lessons for current level
    current_level_lessons = [
        lesson_id for lesson_id, lesson_data in lessons_dict.items()
        if lesson_data['level'] == current_level
    ]

    # Sort alphabetically
    current_level_lessons.sort()

    # Find first uncompleted lesson where ALL prerequisites are met
    for lesson_id in current_level_lessons:
        if lesson_id not in completed_lessons:
            lesson_data = lessons_dict[lesson_id]
            prereqs = lesson_data.get('prerequisites', [])

            # Check if all prerequisites are completed
            if all(prereq in completed_lessons for prereq in prereqs):
                return lesson_id

    return None


def get_lessons_by_level(lessons_dict: dict, level: str) -> List[str]:
    """
    Get all lesson IDs for a specific level.

    Args:
        lessons_dict: Dictionary of all lessons
        level: Level to filter by

    Returns:
        List of lesson IDs for the specified level
    """
    lesson_ids = [
        lesson_id for lesson_id, lesson_data in lessons_dict.items()
        if lesson_data['level'] == level
    ]
    lesson_ids.sort()
    return lesson_ids


def check_prerequisites(
    lesson_data: dict,
    completed_lessons: Set[str]
) -> Tuple[bool, List[str]]:
    """
    Check if all prerequisites for a lesson are met.

    Args:
        lesson_data: Lesson data dictionary
        completed_lessons: Set of completed lesson IDs

    Returns:
        Tuple of (prerequisites_met: bool, missing_prerequisites: list)
    """
    prereqs = lesson_data.get('prerequisites', [])

    if not prereqs:
        return True, []

    missing = [p for p in prereqs if p not in completed_lessons]

    return len(missing) == 0, missing


def find_similar_lessons(
    lesson_name: str,
    lessons_dict: dict,
    max_results: int = 3
) -> List[str]:
    """
    Find lessons with similar names.

    Args:
        lesson_name: The lesson name to search for
        lessons_dict: Dictionary of all lessons
        max_results: Maximum number of results to return

    Returns:
        List of similar lesson IDs
    """
    similar = []
    lesson_name_lower = lesson_name.lower()

    for lesson_id in lessons_dict.keys():
        if lesson_name_lower in lesson_id.lower():
            similar.append(lesson_id)

    return similar[:max_results]


def get_blocked_lessons_info(
    lessons_dict: dict,
    current_level: str,
    completed_lessons: Set[str]
) -> List[Tuple[str, List[str]]]:
    """
    Get information about lessons blocked by prerequisites.

    Args:
        lessons_dict: Dictionary of all lessons
        current_level: User's current level
        completed_lessons: Set of completed lesson IDs

    Returns:
        List of tuples: (lesson_title, missing_prerequisites)
    """
    current_level_lessons = [
        (lid, data) for lid, data in lessons_dict.items()
        if data['level'] == current_level and lid not in completed_lessons
    ]

    blocked = []
    for lesson_id, lesson_data in current_level_lessons:
        prereqs = lesson_data.get('prerequisites', [])
        missing = [p for p in prereqs if p not in completed_lessons]

        if missing:
            blocked.append((lesson_data['title'], missing))

    return blocked


def are_all_lessons_completed(
    lessons_dict: dict,
    current_level: str,
    completed_lessons: Set[str]
) -> bool:
    """
    Check if all lessons at current level are completed.

    Args:
        lessons_dict: Dictionary of all lessons
        current_level: User's current level
        completed_lessons: Set of completed lesson IDs

    Returns:
        True if all lessons at current level are completed
    """
    level_lessons = [
        lid for lid, data in lessons_dict.items()
        if data['level'] == current_level
    ]

    return all(lid in completed_lessons for lid in level_lessons)
