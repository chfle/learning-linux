#!/usr/bin/env python3

import argparse
import sys
import json
import os
from pathlib import Path
from typing import Dict, List, Optional

class LinuxTutor:
    def __init__(self):
        self.config_dir = Path.home() / '.linuxtutor'
        self.progress_file = self.config_dir / 'progress.json'
        self.config_dir.mkdir(exist_ok=True)
        self.progress = self.load_progress()
        
    def load_progress(self) -> Dict:
        if self.progress_file.exists():
            with open(self.progress_file, 'r') as f:
                return json.load(f)
        return {
            'current_level': 'beginner',
            'completed_lessons': [],
            'current_lesson': None,
            'stats': {'lessons_completed': 0, 'exercises_completed': 0},
            'first_time': True
        }
    
    def save_progress(self):
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress, f, indent=2)
    
    def show_status(self):
        level = self.progress['current_level']
        completed = len(self.progress['completed_lessons'])
        print(f"Current Level: {level.title()}")
        print(f"Lessons Completed: {completed}")
        print(f"Exercises Completed: {self.progress['stats']['exercises_completed']}")
        
        if self.progress['current_lesson']:
            print(f"Current Lesson: {self.progress['current_lesson']}")
    
    def list_lessons(self, level: Optional[str] = None):
        from lessons import LESSONS

        # Dynamically build lesson lists from actual lessons
        lessons_by_level = {}
        for lesson_id, lesson_data in LESSONS.items():
            lvl = lesson_data['level']
            if lvl not in lessons_by_level:
                lessons_by_level[lvl] = []
            lessons_by_level[lvl].append(lesson_id)

        # Sort lessons alphabetically within each level
        for lvl in lessons_by_level:
            lessons_by_level[lvl].sort()

        target_level = level or self.progress['current_level']
        if target_level not in lessons_by_level:
            print(f"Invalid level: {target_level}")
            print(f"Available levels: {', '.join(sorted(lessons_by_level.keys()))}")
            return

        print(f"\n{target_level.title()} Level Lessons:")
        for i, lesson in enumerate(lessons_by_level[target_level], 1):
            status = "✓" if lesson in self.progress['completed_lessons'] else "○"
            print(f"  {status} {i}. {lesson.replace('-', ' ').title()}")

    def check_prerequisites(self, lesson_data: dict, lesson_name: str) -> bool:
        """
        Check if user has completed all prerequisites for a lesson.

        Returns True if ready, False if missing prerequisites.
        Prints helpful message if prerequisites missing.
        """
        prereqs = lesson_data.get('prerequisites', [])
        if not prereqs:
            return True

        missing = [p for p in prereqs if p not in self.progress['completed_lessons']]

        if missing:
            print(f"\n⚠️  Cannot start '{lesson_name}' yet.")
            print(f"You need to complete these lessons first:")
            for prereq in missing:
                print(f"  - {prereq.replace('-', ' ').title()}")
            print(f"\nStart with: linuxtutor lesson {missing[0]}")
            return False

        return True

    def show_lesson_not_found_help(self, lesson_name: str):
        """Show helpful error when lesson doesn't exist."""
        from lessons import LESSONS, search_lessons

        print(f"\n❌ Lesson '{lesson_name}' not found.\n")

        # Try fuzzy search for similar lessons
        similar = []
        for lesson_id in LESSONS.keys():
            if lesson_name.lower() in lesson_id.lower():
                similar.append(lesson_id)

        if similar:
            print("Did you mean:")
            for s in similar[:3]:
                print(f"  - {s}")
            print()

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
        print(f"  linuxtutor lessons           # Browse all available lessons")
        print(f"  linuxtutor search {lesson_name}   # Search for related lessons")
        print(f"  linuxtutor lessons beginner  # Start with beginner lessons")

    def start_lesson(self, lesson_name: str):
        from lessons import get_lesson

        lesson = get_lesson(lesson_name)
        if not lesson:
            self.show_lesson_not_found_help(lesson_name)
            return

        # Check prerequisites
        if not self.check_prerequisites(lesson, lesson_name):
            return

        self.progress['current_lesson'] = lesson_name
        self.save_progress()

        print(f"\n=== {lesson['title']} ===")
        print(f"Level: {lesson['level'].title()}")
        print(f"Duration: ~{lesson['duration']} minutes\n")
        print(lesson['description'])

        if lesson.get('prerequisites'):
            print(f"\nPrerequisites: {', '.join(lesson['prerequisites'])}")

        print(f"\nTo continue with this lesson, run:")
        print(f"  linuxtutor lesson {lesson_name} --continue")
    
    def continue_lesson(self, lesson_name: str):
        from lessons import get_lesson, run_lesson

        lesson = get_lesson(lesson_name)
        if not lesson:
            self.show_lesson_not_found_help(lesson_name)
            return

        # Check prerequisites
        if not self.check_prerequisites(lesson, lesson_name):
            return

        run_lesson(lesson, self)
    
    def complete_lesson(self, lesson_name: str):
        if lesson_name not in self.progress['completed_lessons']:
            self.progress['completed_lessons'].append(lesson_name)
            self.progress['stats']['lessons_completed'] += 1
            
        self.progress['current_lesson'] = None
        self.save_progress()
        print(f"✓ Completed lesson: {lesson_name}")
    
    def set_level(self, level: str):
        valid_levels = ['beginner', 'intermediate', 'advanced', 'expert']
        if level not in valid_levels:
            print(f"Invalid level. Choose from: {', '.join(valid_levels)}")
            return

        self.progress['current_level'] = level
        self.save_progress()
        print(f"Level set to: {level}")

    def search_lessons(self, keywords: List[str], level_filter: Optional[str] = None):
        """
        Search for lessons matching keywords and display results.

        Args:
            keywords: List of search terms
            level_filter: Optional level filter (beginner/intermediate/advanced/expert)
        """
        from lessons import search_lessons as search_fn

        # Validate input
        if not keywords:
            print("Error: Please provide at least one keyword to search for.")
            print("Usage: linuxtutor search <keyword> [<keyword2> ...]")
            return

        # Perform search
        results = search_fn(keywords)

        # Apply level filter if specified
        if level_filter:
            results = [r for r in results if r['lesson_data']['level'] == level_filter]

        # Handle no results
        if not results:
            print(f"\nNo lessons found matching: {', '.join(keywords)}")
            print("\nTry:")
            print("  - Using fewer or different keywords")
            if level_filter:
                print(f"  - Searching without --level filter")
            print("  - Running 'linuxtutor lessons' to browse all lessons")
            return

        # Display results
        plural = 's' if len(results) != 1 else ''
        print(f"\nFound {len(results)} lesson{plural} matching: {', '.join(keywords)}\n")

        for i, result in enumerate(results, 1):
            lesson = result['lesson_data']
            lesson_id = result['lesson_id']

            # Check completion status
            status = "" if lesson_id in self.progress['completed_lessons'] else " "

            # Header line
            print(f"{i}. [{lesson['level'].title()}] {lesson['title']} (Score: {result['score']})")
            print(f"   Duration: {lesson['duration']} minutes")
            print(f"   Matched in: {', '.join(sorted(result['fields_matched']))}")

            # Show snippets
            snippets_shown = 0
            max_snippets = 2  # Limit snippets per result

            # Prioritize description snippet
            if 'description' in result['snippets'] and snippets_shown < max_snippets:
                print(f"\n   Description:")
                print(f"   \"{result['snippets']['description']}\"")
                snippets_shown += 1

            # Show section title snippet
            if 'section_title' in result['snippets'] and snippets_shown < max_snippets:
                print(f"\n   Section:")
                print(f"   \"{result['snippets']['section_title']}\"")
                snippets_shown += 1

            # Show text snippet if we haven't shown enough
            if 'text' in result['snippets'] and snippets_shown < max_snippets:
                print(f"\n   Content:")
                print(f"   \"{result['snippets']['text']}\"")
                snippets_shown += 1

            # Show command description snippet
            if 'command_desc' in result['snippets'] and snippets_shown < max_snippets:
                print(f"\n   Command:")
                print(f"   \"{result['snippets']['command_desc']}\"")
                snippets_shown += 1

            print()  # Blank line between results

        # Helpful hint
        print(f"To start a lesson, run: linuxtutor lesson <lesson-name>")

    def start_learning(self):
        """Smart start command that handles new and returning users"""
        is_first_time = self.progress.get('first_time', True)
        
        if is_first_time:
            self.show_welcome()
            self.progress['first_time'] = False
            self.save_progress()
        else:
            self.show_continue_options()
    
    def show_welcome(self):
        """Welcome message for first-time users"""
        print("🐧 Welcome to LinuxTutor!")
        print("=" * 50)
        print("\nYou're about to start your Linux learning journey!")
        print("LinuxTutor will guide you from complete beginner to Linux expert.")
        print("\nHere's how it works:")
        print("• Progressive lessons from beginner to expert level")
        print("• Hands-on exercises with real commands")
        print("• Your progress is automatically saved")
        print("• Safe practice environment")
        
        print(f"\nYour progress will be saved in: {self.config_dir}")
        
        choice = input("\nReady to start your first lesson? [Y/n]: ").lower().strip()
        
        if choice in ['', 'y', 'yes']:
            print("\n🚀 Let's begin with the basics!")
            self.start_lesson('intro-to-terminal')
            print(f"\nTo continue this lesson interactively, run:")
            print(f"  linuxtutor lesson intro-to-terminal --continue")
            print(f"\nOr simply run 'linuxtutor start' anytime to continue where you left off!")
        else:
            print("\nNo problem! When you're ready, run:")
            print("  linuxtutor start")
            print("  linuxtutor lessons    # to see all available lessons")
            print("  linuxtutor help       # for more options")
    
    def show_continue_options(self):
        """Smart continuation for returning users"""
        current_lesson = self.progress.get('current_lesson')
        completed_count = len(self.progress['completed_lessons'])
        level = self.progress['current_level']
        
        print("🐧 Welcome back to LinuxTutor!")
        print("=" * 40)
        
        if current_lesson:
            print(f"📖 You have an ongoing lesson: {current_lesson.replace('-', ' ').title()}")
            choice = input("Continue this lesson? [Y/n]: ").lower().strip()
            
            if choice in ['', 'y', 'yes']:
                self.continue_lesson(current_lesson)
                return
        
        if completed_count == 0:
            print("🎯 You haven't completed any lessons yet.")
            print("Let's start with the basics!")
            self.start_lesson('intro-to-terminal')
            print(f"\nTo continue this lesson interactively, run:")
            print(f"  linuxtutor lesson intro-to-terminal --continue")
        else:
            print(f"📊 Progress: {completed_count} lessons completed ({level} level)")
            
            # Suggest next lesson
            next_lesson = self.get_next_lesson()
            if next_lesson:
                print(f"📚 Suggested next lesson: {next_lesson.replace('-', ' ').title()}")
                choice = input("Start this lesson? [Y/n]: ").lower().strip()
                
                if choice in ['', 'y', 'yes']:
                    self.start_lesson(next_lesson)
                    print(f"\nTo continue this lesson interactively, run:")
                    print(f"  linuxtutor lesson {next_lesson} --continue")
                else:
                    print("\nOther options:")
                    print("  linuxtutor lessons    # see all lessons")
                    print("  linuxtutor status     # check your progress")
            else:
                print("🎉 Congratulations! You've completed all lessons in your current level.")
                self.suggest_level_up()
    
    def get_next_lesson(self) -> Optional[str]:
        """Find the next uncompleted lesson in current level"""
        lessons = {
            'beginner': [
                'intro-to-terminal', 'file-system-basics', 'basic-commands',
                'file-permissions', 'text-editors'
            ],
            'intermediate': [
                'process-management', 'text-processing', 'file-operations',
                'networking-basics', 'package-management'
            ],
            'advanced': [
                'shell-scripting', 'system-administration', 'log-analysis',
                'security-basics', 'performance-monitoring'
            ],
            'expert': [
                'kernel-concepts', 'advanced-networking', 'performance-tuning',
                'security-hardening', 'automation-deployment'
            ]
        }
        
        current_level_lessons = lessons.get(self.progress['current_level'], [])
        completed = set(self.progress['completed_lessons'])
        
        for lesson in current_level_lessons:
            if lesson not in completed:
                return lesson
        
        return None
    
    def suggest_level_up(self):
        """Suggest moving to next level"""
        level_progression = ['beginner', 'intermediate', 'advanced', 'expert']
        current_level = self.progress['current_level']
        
        try:
            current_index = level_progression.index(current_level)
            if current_index < len(level_progression) - 1:
                next_level = level_progression[current_index + 1]
                print(f"\n🎓 Ready to level up to {next_level.title()}?")
                choice = input("Move to next level? [Y/n]: ").lower().strip()
                
                if choice in ['', 'y', 'yes']:
                    self.set_level(next_level)
                    next_lesson = self.get_next_lesson()
                    if next_lesson:
                        print(f"\n🚀 Starting your first {next_level} lesson!")
                        self.start_lesson(next_lesson)
            else:
                print("🏆 Amazing! You've mastered all Linux levels!")
                print("Consider contributing to the project or mentoring others!")
        except ValueError:
            pass
    
    def show_help(self):
        help_text = """
LinuxTutor - Interactive Linux Learning CLI

Commands:
  start                     Smart start - perfect for new and returning users!
  status                    Show current progress and level
  lessons [level]          List available lessons (for current or specified level)
  lesson <name>            Start a lesson
  lesson <name> --continue Continue an interactive lesson
  level <level>            Set current learning level
  search <keywords>...     Search lessons by keyword (AND logic)
                          Use --level to filter by difficulty
  help                     Show this help message

Levels: beginner, intermediate, advanced, expert

Examples:
  linuxtutor start         # 👈 Best way to start!
  linuxtutor status
  linuxtutor lessons beginner
  linuxtutor lesson intro-to-terminal
  linuxtutor level intermediate
  linuxtutor search file security
  linuxtutor search process --level intermediate
        """
        print(help_text.strip())

def main():
    parser = argparse.ArgumentParser(description='LinuxTutor - Interactive Linux Learning')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Start command - the main entry point!
    subparsers.add_parser('start', help='Smart start - perfect for new and returning users!')
    
    # Status command
    subparsers.add_parser('status', help='Show current progress')
    
    # Lessons command
    lessons_parser = subparsers.add_parser('lessons', help='List available lessons')
    lessons_parser.add_argument('level', nargs='?', help='Specific level to show')
    
    # Lesson command
    lesson_parser = subparsers.add_parser('lesson', help='Start or continue a lesson')
    lesson_parser.add_argument('name', help='Lesson name')
    lesson_parser.add_argument('--continue', action='store_true', dest='continue_lesson', help='Continue interactive lesson')
    
    # Level command
    level_parser = subparsers.add_parser('level', help='Set current learning level')
    level_parser.add_argument('level', help='Learning level (beginner/intermediate/advanced/expert)')
    
    # Help command
    subparsers.add_parser('help', help='Show detailed help')

    # Search command
    search_parser = subparsers.add_parser('search', help='Search lessons by keyword')
    search_parser.add_argument('keywords', nargs='+', help='Keywords to search for (AND logic)')
    search_parser.add_argument('--level', '-l',
                              choices=['beginner', 'intermediate', 'advanced', 'expert'],
                              help='Filter results by level')

    args = parser.parse_args()
    
    tutor = LinuxTutor()
    
    # If no command provided, show the smart start for new users
    if len(sys.argv) == 1:
        is_first_time = tutor.progress.get('first_time', True)
        if is_first_time:
            print("🐧 Welcome to LinuxTutor!")
            print("To get started, run: linuxtutor start")
        else:
            print("🐧 LinuxTutor - Interactive Linux Learning")
            print("Run 'linuxtutor start' to continue learning or 'linuxtutor help' for options.")
        return
    
    if args.command == 'start':
        tutor.start_learning()
    elif args.command == 'status':
        tutor.show_status()
    elif args.command == 'lessons':
        tutor.list_lessons(args.level)
    elif args.command == 'lesson':
        if args.continue_lesson:
            tutor.continue_lesson(args.name)
        else:
            tutor.start_lesson(args.name)
    elif args.command == 'level':
        tutor.set_level(args.level)
    elif args.command == 'help':
        tutor.show_help()
    elif args.command == 'search':
        tutor.search_lessons(args.keywords, args.level)

if __name__ == '__main__':
    main()