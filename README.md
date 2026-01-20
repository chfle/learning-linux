# LinuxTutor

A comprehensive interactive command-line learning platform for mastering Linux from beginner to expert level. This educational tool provides structured lessons, hands-on exercises, and progress tracking to help users develop essential Linux command line skills through practical experience.

## Features

- **Progressive Learning**: Four skill levels from beginner to expert
- **Interactive Lessons**: Step-by-step tutorials with practical exercises
- **Safe Practice Environment**: Simulated commands for safe learning
- **Progress Tracking**: Keep track of completed lessons and achievements
- **Comprehensive Coverage**: Topics from basic navigation to advanced system administration
- **Smart Search**: Full-text search across all lessons with relevance ranking and context snippets

## Quick Start

### Installation

1. Clone or download this repository
2. Run the setup script:
```bash
python3 setup.py
```

3. If `~/.local/bin` isn't in your PATH, add it:
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Basic Usage

```bash
# The easiest way to start (perfect for new users!)
linuxtutor start

# Other useful commands:
linuxtutor status                        # Check your progress
linuxtutor lessons                       # List available lessons
linuxtutor lesson intro-to-terminal      # Start a specific lesson
linuxtutor level intermediate            # Change your skill level
linuxtutor search file security          # Search lessons by keywords
linuxtutor search process --level intermediate  # Search with level filter
linuxtutor help                          # Get help
```

## Learning Path

### Beginner Level
- **intro-to-terminal**: Introduction to the Terminal
- **file-system-basics**: Linux File System Basics  
- **basic-commands**: Essential Linux Commands
- **file-permissions**: Understanding File Permissions
- **text-editors**: Working with Text Editors

### Intermediate Level
- **process-management**: Process Management
- **text-processing**: Text Processing Tools
- **file-operations**: Advanced File Operations
- **networking-basics**: Basic Networking Commands
- **package-management**: Package Management

### Advanced Level
- **shell-scripting**: Introduction to Shell Scripting
- **system-administration**: System Administration
- **log-analysis**: Log File Analysis
- **security-basics**: Linux Security Fundamentals
- **performance-monitoring**: Performance Monitoring

### Expert Level
- **kernel-concepts**: Linux Kernel Concepts
- **advanced-networking**: Advanced Networking
- **performance-tuning**: Linux Performance Tuning
- **security-hardening**: Security Hardening
- **automation-deployment**: Automation and Deployment

## How It Works

LinuxTutor creates a personalized learning experience:

1. **Progress Tracking**: Your progress is saved in `~/.linuxtutor/progress.json`
2. **Safe Learning**: Commands are simulated or run safely to prevent system damage
3. **Interactive Exercises**: Practice real commands with guided explanations
4. **Structured Path**: Prerequisites ensure you build knowledge progressively

## Project Structure

```
learning-linux/
├── .github/
│   └── workflows/
│       └── ci.yml         # GitHub Actions CI pipeline
├── tests/                 # Test suite directory
│   ├── __init__.py        # Test package initialization
│   ├── test_search.py     # Search feature tests (47 tests)
│   └── test_lessons.py    # Lesson structure and validation tests (26 tests)
├── linuxtutor.py          # Main CLI application
├── lessons.py             # Lesson content and exercises (9 lessons)
├── run_tests.py           # Automated test runner with discovery
├── validate_syntax.py     # Python syntax validator
├── setup.py               # Installation script
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## Advanced Usage

### Manual Installation
If you prefer not to use the setup script:

```bash
# Make the script executable
chmod +x linuxtutor.py

# Run directly
./linuxtutor.py help

# Or with Python
python3 linuxtutor.py help
```

### Uninstall
```bash
python3 setup.py uninstall
```

## Development & Testing

### Running Tests

LinuxTutor includes a comprehensive automated test suite with intelligent test discovery:

```bash
# Run all tests (automatically discovers all test_*.py files)
python3 run_tests.py

# Run with verbose output
python3 run_tests.py -v

# Run with very verbose output
python3 run_tests.py -vv

# Run specific test pattern
python3 run_tests.py --pattern "test_search.py"

# Stop on first failure
python3 run_tests.py --failfast

# Quiet mode (minimal output)
python3 run_tests.py -q
```

**Current test coverage: 73 tests**
- Search functionality (snippet extraction, scoring, AND logic)
- Relevance ranking and result sorting
- Level filtering
- Lesson structure validation and content
- Prerequisite validation and enforcement
- Error messages and user guidance
- Dynamic lesson listing
- Edge cases and error handling
- Integration tests

**Adding new tests**: Simply create a new file in `tests/` starting with `test_` and the test runner will automatically discover and run it!

### Code Quality Validation

Automatically validate Python syntax for all files in the project:

```bash
# Validate all Python files
python3 validate_syntax.py

# Verbose mode (shows all files being checked)
python3 validate_syntax.py --verbose

# Exclude specific directories
python3 validate_syntax.py --exclude venv build dist
```

The validator automatically discovers all `.py` files and checks for syntax errors.

### Continuous Integration

This project uses GitHub Actions for automated testing. Every push and pull request automatically:

**Multi-version Testing:**
- Tests on Python 3.8, 3.9, 3.10, 3.11, and 3.12
- Runs automated test discovery and execution
- Validates CLI commands work correctly

**Code Quality:**
- Validates Python syntax for ALL files (auto-discovery)
- Runs flake8 linting
- Checks code complexity and standards

**Integration Tests:**
- Tests complete CLI workflow
- Validates project structure
- Ensures all tools are functional

**Why this is scalable:** No hardcoded file lists! As you add more test files or Python modules, the CI pipeline automatically discovers and validates them.

### Adding New Tests

1. Create a new test file in `tests/` directory (must start with `test_`)
2. Write your tests using `unittest`
3. Run `python3 run_tests.py` - your tests are automatically discovered!

Example:
```bash
# Create new test file
touch tests/test_lessons.py

# The test runner will automatically find and run it
python3 run_tests.py
```

## Contributing

This is a learning project that can be extended with lots of cool features!

**Current Status:**
- ✅ Beginner track complete (5/5 lessons)
- ✅ Dynamic lesson system with prerequisite validation
- ✅ Full-text search with relevance ranking
- 🚧 9 of 20 lessons implemented

Here's our wishlist:

### High Priority
- [ ] quiz system - add some questions after lessons so ppl actually learn stuff
- [ ] safe command simulator - tired of people breaking their systems lol
- [ ] Docker integration - each lesson in container (IMPORTANT)
- [ ] HACKER LEVEL - kernel exploits, rootkits, reverse eng (the fun stuff)
- [ ] red team track - pentest, social eng, osint
- [ ] docker labs for every lesson - isolated environments
- [ ] vulnerable VMs for hacking practice (legally obvs)
- [ ] CTF challenges - real security scenarios with flags
- [ ] advanced docker security - container escapes, privesc

### Medium Priority
- [ ] gamification would be cool - badges, streaks, maybe points?
- [ ] difficulty ratings + adaptive paths based on how user is doing
- [ ] integrate with man pages - linuxtutor man ls or something
- [x] search lessons by keyword - DONE! Full-text search with relevance ranking
- [ ] distro-specific content - ubuntu vs arch commands are different
- [ ] track how long lessons take, performance metrics
- [ ] practice challenges / competitions - make it fun
- [ ] lesson feedback system - let users rate lessons
- [ ] community content tools - let others write lessons
- [ ] smarter prereq checking - don't let noobs jump to advanced
- [ ] kubernetes module - containers are huge now
- [ ] defensive security - malware analysis, incident response
- [ ] cloud pentest modules - aws/azure/gcp security
- [ ] network forensics + wireshark training

### Nice to Have
- [ ] certificates for completing stuff (people love showing off)
- [ ] progress charts in terminal would look sick
- [ ] bookmark favorite lessons
- [ ] multi-language support (spanish, french, etc)
- [ ] group learning features??? maybe overkill
- [ ] export progress to pdf/csv - managers love reports
- [ ] accessibility - voice narration for blind users

## Example Sessions

### First-Time User
```bash
$ linuxtutor start
Welcome to LinuxTutor!
==================================================

You're about to start your Linux learning journey!
LinuxTutor will guide you from complete beginner to Linux expert.

Here's how it works:
• Progressive lessons from beginner to expert level
• Hands-on exercises with real commands
• Your progress is automatically saved
• Safe practice environment

Ready to start your first lesson? [Y/n]: y

Let's begin with the basics!
=== Introduction to the Terminal ===
Level: Beginner
Duration: ~15 minutes
...
```

### Returning User
```bash
$ linuxtutor start
Welcome back to LinuxTutor!
========================================
You have an ongoing lesson: File System Basics
Continue this lesson? [Y/n]: y

==================================================
Starting: Linux File System Basics
==================================================
...
```

### Searching for Lessons
```bash
$ linuxtutor search file security
Found 1 lesson matching: file, security

1. [Advanced] Linux Security Fundamentals (Score: 28)
   Duration: 40 minutes
   Matched in: title, description, section_title, text, command_desc

   Description:
   "Learn essential Linux security concepts and best practices."

   Section:
   "Linux Security Concepts"

To start a lesson, run: linuxtutor lesson <lesson-name>
```

## Search Feature

The search command helps you quickly find relevant lessons:

- **Full-text search**: Searches titles, descriptions, section names, commands, and lesson content
- **Multiple keywords**: Use AND logic - all keywords must match
- **Relevance ranking**: Results sorted by relevance (title matches ranked highest)
- **Context snippets**: See where your keywords appear in the lesson
- **Level filtering**: Use `--level` or `-l` to filter by difficulty

**Examples:**
```bash
linuxtutor search file                    # Find lessons about files
linuxtutor search file security           # Find lessons with both keywords
linuxtutor search process --level intermediate  # Search intermediate lessons only
linuxtutor search shell script -l advanced      # Short flag version
```

## License

This project is created for educational purposes. Feel free to use, modify, and distribute.

---

**Happy Learning!**

Start your Linux journey today with:
```bash
linuxtutor start
```
