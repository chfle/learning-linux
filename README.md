# LinuxTutor 🐧

An interactive CLI application for learning Linux from basics to expert level. LinuxTutor provides structured lessons, hands-on exercises, and progress tracking to help you master Linux command line skills.

## Features

- **Progressive Learning**: Four skill levels from beginner to expert
- **Interactive Lessons**: Step-by-step tutorials with practical exercises
- **Safe Practice Environment**: Simulated commands for safe learning
- **Progress Tracking**: Keep track of completed lessons and achievements
- **Comprehensive Coverage**: Topics from basic navigation to advanced system administration

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
# 🚀 The easiest way to start (perfect for new users!)
linuxtutor start

# Other useful commands:
linuxtutor status                        # Check your progress
linuxtutor lessons                       # List available lessons
linuxtutor lesson intro-to-terminal      # Start a specific lesson
linuxtutor level intermediate            # Change your skill level
linuxtutor help                          # Get help
```

## Learning Path

### 🟢 Beginner Level
- **intro-to-terminal**: Introduction to the Terminal
- **file-system-basics**: Linux File System Basics  
- **basic-commands**: Essential Linux Commands
- **file-permissions**: Understanding File Permissions
- **text-editors**: Working with Text Editors

### 🟡 Intermediate Level
- **process-management**: Process Management
- **text-processing**: Text Processing Tools
- **file-operations**: Advanced File Operations
- **networking-basics**: Basic Networking Commands
- **package-management**: Package Management

### 🟠 Advanced Level
- **shell-scripting**: Introduction to Shell Scripting
- **system-administration**: System Administration
- **log-analysis**: Log File Analysis
- **security-basics**: Linux Security Fundamentals
- **performance-monitoring**: Performance Monitoring

### 🔴 Expert Level
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
├── linuxtutor.py      # Main CLI application
├── lessons.py         # Lesson content and exercises
├── setup.py          # Installation script
└── README.md         # This file
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

## Contributing

This is a learning project that can be extended with:
- Additional lesson content
- More interactive exercises
- Quiz systems
- Achievement badges
- Integration with real Linux environments

## Example Sessions

### First-Time User
```bash
$ linuxtutor start
🐧 Welcome to LinuxTutor!
==================================================

You're about to start your Linux learning journey!
LinuxTutor will guide you from complete beginner to Linux expert.

Here's how it works:
• Progressive lessons from beginner to expert level
• Hands-on exercises with real commands
• Your progress is automatically saved
• Safe practice environment

Ready to start your first lesson? [Y/n]: y

🚀 Let's begin with the basics!
=== Introduction to the Terminal ===
Level: Beginner
Duration: ~15 minutes
...
```

### Returning User
```bash
$ linuxtutor start
🐧 Welcome back to LinuxTutor!
========================================
📖 You have an ongoing lesson: File System Basics
Continue this lesson? [Y/n]: y

==================================================
Starting: Linux File System Basics
==================================================
...
```

## License

This project is created for educational purposes. Feel free to use, modify, and distribute.

---

**Happy Learning!** 🚀

Start your Linux journey today with:
```bash
linuxtutor start
```