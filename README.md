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

This is a learning project that can be extended with lots of cool features! Here's our wishlist:

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
- [ ] search lessons by keyword - basic feature we're missing
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