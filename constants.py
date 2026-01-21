"""Application-wide constants and configuration."""

from typing import List

# Skill levels
LEVEL_BEGINNER = 'beginner'
LEVEL_INTERMEDIATE = 'intermediate'
LEVEL_ADVANCED = 'advanced'
LEVEL_EXPERT = 'expert'

VALID_LEVELS: List[str] = [
    LEVEL_BEGINNER,
    LEVEL_INTERMEDIATE,
    LEVEL_ADVANCED,
    LEVEL_EXPERT
]

# Progress file configuration
CONFIG_DIR_NAME = '.linuxtutor'
PROGRESS_FILE_NAME = 'progress.json'

# Display formatting
SEPARATOR_LIGHT = '=' * 40
SEPARATOR_MEDIUM = '=' * 50
SEPARATOR_HEAVY = '=' * 60

CHECKBOX_COMPLETED = '[X]'
CHECKBOX_PENDING = '[ ]'

# Default values
DEFAULT_LEVEL = LEVEL_BEGINNER
DEFAULT_FIRST_TIME = True

# Positive responses for yes/no prompts
AFFIRMATIVE_RESPONSES = ['', 'y', 'yes']

# Quiz display symbols
QUIZ_CHECKMARK = '✓'
QUIZ_CROSSMARK = '✗'
QUIZ_SEPARATOR = '─' * 40
