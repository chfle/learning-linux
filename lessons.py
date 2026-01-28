import os
import sys
import subprocess
from typing import Dict, List, Optional, Any
from quiz_system import Quiz, QuizRunner
from ui_prompts import prompt_yes_no

LESSONS = {
    'intro-to-terminal': {
        'title': 'Introduction to the Terminal',
        'level': 'beginner',
        'duration': 15,
        'description': 'Learn the basics of the Linux terminal and command line interface.',
        'prerequisites': [],
        'content': [
            {
                'type': 'explanation',
                'title': 'What is the Terminal?',
                'text': '''The terminal (also called command line or shell) is a text-based interface
for interacting with your Linux system. Unlike graphical interfaces, you type commands
to perform tasks. This might seem intimidating at first, but it's incredibly powerful
and efficient once you learn the basics.'''
            },
            {
                'type': 'exercise',
                'title': 'Your First Commands',
                'instructions': 'Try these basic commands:',
                'commands': [
                    {'cmd': 'whoami', 'description': 'Shows your current username'},
                    {'cmd': 'pwd', 'description': 'Shows your current directory (Print Working Directory)'},
                    {'cmd': 'date', 'description': 'Shows the current date and time'},
                    {'cmd': 'uname -a', 'description': 'Shows system information'}
                ]
            }
        ],
        'quiz': [
            {
                'type': 'multiple_choice',
                'question': 'What does the terminal allow you to do?',
                'options': [
                    'Interact with Linux using text commands',
                    'Only view files',
                    'Browse the internet',
                    'Create graphics'
                ],
                'correct': 0,
                'explanation': 'The terminal is a text-based interface for interacting with your Linux system using commands.'
            },
            {
                'type': 'command_recall',
                'question': 'Which command displays your current username?',
                'answer': 'whoami',
                'explanation': 'The whoami command shows your current username.'
            },
            {
                'type': 'command_recall',
                'question': 'Which command shows your current directory location?',
                'answer': 'pwd',
                'explanation': 'pwd stands for Print Working Directory and shows your current location in the file system.'
            },
            {
                'type': 'true_false',
                'question': 'The terminal can only be used by experts.',
                'answer': False,
                'explanation': 'False. While it may seem intimidating at first, anyone can learn to use the terminal with practice.'
            },
            {
                'type': 'multiple_choice',
                'question': 'What does pwd stand for?',
                'options': [
                    'Print Working Directory',
                    'Power Working Drive',
                    'Present Working Data',
                    'Process Window Display'
                ],
                'correct': 0,
                'explanation': 'pwd stands for Print Working Directory.'
            },
            {
                'type': 'command_recall',
                'question': 'Which command shows the current date and time?',
                'answer': 'date',
                'explanation': 'The date command displays the current date and time.'
            },
            {
                'type': 'multiple_choice',
                'question': 'What is another name for the terminal?',
                'options': [
                    'Command line or shell',
                    'Desktop',
                    'File manager',
                    'Web browser'
                ],
                'correct': 0,
                'explanation': 'The terminal is also called the command line or shell.'
            },
            {
                'type': 'true_false',
                'question': 'The uname command shows system information.',
                'answer': True,
                'explanation': 'True. The uname command (especially with -a flag) displays system information.'
            },
            {
                'type': 'multiple_choice',
                'question': 'Why is the terminal powerful once you learn it?',
                'options': [
                    'It allows efficient task automation and system control',
                    'It has colorful graphics',
                    'It is easier than using a mouse',
                    'It requires no learning'
                ],
                'correct': 0,
                'explanation': 'The terminal is powerful because it enables efficient automation and precise system control.'
            },
            {
                'type': 'true_false',
                'question': 'Commands in the terminal are typed as text.',
                'answer': True,
                'explanation': 'True. The terminal is a text-based interface where you type commands.'
            }
        ]
    },
    
    'file-system-basics': {
        'title': 'Linux File System Basics',
        'level': 'beginner',
        'duration': 20,
        'description': 'Understand the Linux file system hierarchy and navigation.',
        'prerequisites': ['intro-to-terminal'],
        'content': [
            {
                'type': 'explanation',
                'title': 'Linux File System Hierarchy',
                'text': '''Linux uses a hierarchical file system that starts at the root directory (/).
Key directories include:
- /home - User home directories
- /etc - System configuration files
- /var - Variable data (logs, temporary files)
- /usr - User programs and utilities
- /bin - Essential system binaries
- /tmp - Temporary files'''
            },
            {
                'type': 'exercise',
                'title': 'Navigation Commands',
                'instructions': 'Practice these navigation commands:',
                'commands': [
                    {'cmd': 'ls', 'description': 'List files and directories'},
                    {'cmd': 'ls -la', 'description': 'List files with detailed information and hidden files'},
                    {'cmd': 'cd /home', 'description': 'Change to the /home directory'},
                    {'cmd': 'cd ~', 'description': 'Change to your home directory'},
                    {'cmd': 'cd ..', 'description': 'Go up one directory level'},
                    {'cmd': 'cd -', 'description': 'Go back to the previous directory'}
                ]
            }
        ],
        'quiz': [
            {
                'type': 'multiple_choice',
                'question': 'What is the root directory in Linux?',
                'options': [
                    '/',
                    '/root',
                    '/home',
                    'C:\\'
                ],
                'correct': 0,
                'explanation': 'The root directory is represented by a single forward slash (/).'
            },
            {
                'type': 'multiple_choice',
                'question': 'Which directory contains user home directories?',
                'options': [
                    '/home',
                    '/users',
                    '/usr',
                    '/var'
                ],
                'correct': 0,
                'explanation': '/home contains home directories for all regular users.'
            },
            {
                'type': 'multiple_choice',
                'question': 'Where are system configuration files typically stored?',
                'options': [
                    '/etc',
                    '/config',
                    '/sys',
                    '/settings'
                ],
                'correct': 0,
                'explanation': '/etc contains system-wide configuration files.'
            },
            {
                'type': 'command_recall',
                'question': 'Which command is used to change directories?',
                'answer': 'cd',
                'explanation': 'cd (change directory) is used to navigate between directories.'
            },
            {
                'type': 'command_recall',
                'question': 'What command lists files and directories?',
                'answer': 'ls',
                'alternatives': ['ls -l', 'ls -la'],
                'explanation': 'ls lists directory contents. Common variants include ls -l and ls -la.'
            },
            {
                'type': 'fill_blank',
                'question': 'The ~ symbol represents your _____ directory.',
                'answer': 'home',
                'explanation': 'The tilde (~) is a shortcut for your home directory.'
            },
            {
                'type': 'true_false',
                'question': '/tmp stores temporary files that may be deleted on reboot.',
                'answer': True,
                'explanation': 'True. /tmp is designed for temporary files and is often cleared on reboot.'
            },
            {
                'type': 'multiple_choice',
                'question': 'What does "cd .." do?',
                'options': [
                    'Moves up one directory level',
                    'Moves down one directory level',
                    'Goes to the root directory',
                    'Lists the current directory'
                ],
                'correct': 0,
                'explanation': '"cd .." moves up to the parent directory.'
            },
            {
                'type': 'true_false',
                'question': '/bin contains essential system commands and binaries.',
                'answer': True,
                'explanation': 'True. /bin stores essential binary executables needed for system operation.'
            },
            {
                'type': 'multiple_choice',
                'question': 'Which directory contains variable data like logs?',
                'options': [
                    '/var',
                    '/log',
                    '/data',
                    '/tmp'
                ],
                'correct': 0,
                'explanation': '/var (variable) stores data that changes frequently, including logs.'
            }
        ]
    },
    
    'basic-commands': {
        'title': 'Essential Linux Commands',
        'level': 'beginner',
        'duration': 25,
        'description': 'Master the most commonly used Linux commands.',
        'prerequisites': ['file-system-basics'],
        'content': [
            {
                'type': 'explanation',
                'title': 'File and Directory Operations',
                'text': '''These commands form the foundation of file system interaction:
- Creating: mkdir, touch
- Copying: cp
- Moving/Renaming: mv
- Removing: rm, rmdir
- Viewing: cat, less, head, tail'''
            },
            {
                'type': 'exercise',
                'title': 'File Operations Practice',
                'instructions': 'Try these file operations (be careful with rm!):',
                'commands': [
                    {'cmd': 'mkdir test_dir', 'description': 'Create a directory named test_dir'},
                    {'cmd': 'touch test_file.txt', 'description': 'Create an empty file'},
                    {'cmd': 'echo "Hello Linux" > test_file.txt', 'description': 'Write text to a file'},
                    {'cmd': 'cat test_file.txt', 'description': 'Display file contents'},
                    {'cmd': 'cp test_file.txt test_copy.txt', 'description': 'Copy a file'},
                    {'cmd': 'mv test_copy.txt test_dir/', 'description': 'Move file to directory'},
                    {'cmd': 'ls test_dir/', 'description': 'List contents of directory'}
                ]
            }
        ],
        'quiz': [
            {
                'type': 'command_recall',
                'question': 'Which command creates a new directory?',
                'answer': 'mkdir',
                'explanation': 'mkdir (make directory) creates new directories.'
            },
            {
                'type': 'command_recall',
                'question': 'Which command creates an empty file?',
                'answer': 'touch',
                'explanation': 'touch creates empty files or updates file timestamps.'
            },
            {
                'type': 'multiple_choice',
                'question': 'What does the cp command do?',
                'options': [
                    'Copies files or directories',
                    'Changes permissions',
                    'Creates a process',
                    'Compares files'
                ],
                'correct': 0,
                'explanation': 'cp (copy) duplicates files or directories.'
            },
            {
                'type': 'multiple_choice',
                'question': 'What is the difference between mv and cp?',
                'options': [
                    'mv moves/renames, cp copies',
                    'mv copies, cp moves',
                    'They are the same',
                    'mv is faster than cp'
                ],
                'correct': 0,
                'explanation': 'mv moves or renames files, while cp creates a copy.'
            },
            {
                'type': 'command_recall',
                'question': 'Which command displays the contents of a text file?',
                'answer': 'cat',
                'alternatives': ['less', 'more', 'head', 'tail'],
                'explanation': 'cat displays file contents. less, more, head, and tail are also valid viewers.'
            },
            {
                'type': 'true_false',
                'question': 'The rm command can be dangerous because it permanently deletes files.',
                'answer': True,
                'explanation': 'True. rm removes files permanently without moving them to a trash/recycle bin.'
            },
            {
                'type': 'multiple_choice',
                'question': 'How do you remove an empty directory?',
                'options': [
                    'rmdir directory_name',
                    'rm directory_name',
                    'delete directory_name',
                    'remove directory_name'
                ],
                'correct': 0,
                'explanation': 'rmdir removes empty directories. Use rm -r for non-empty directories.'
            },
            {
                'type': 'fill_blank',
                'question': 'The _____ command can view the first few lines of a file.',
                'answer': 'head',
                'explanation': 'head displays the first lines of a file (default 10 lines).'
            },
            {
                'type': 'fill_blank',
                'question': 'The _____ command can view the last few lines of a file.',
                'answer': 'tail',
                'explanation': 'tail displays the last lines of a file (default 10 lines).'
            },
            {
                'type': 'true_false',
                'question': 'The mv command can be used to rename files.',
                'answer': True,
                'explanation': 'True. mv can both move files to new locations and rename them.'
            }
        ]
    },
    
    'process-management': {
        'title': 'Process Management',
        'level': 'intermediate',
        'duration': 30,
        'description': 'Learn to monitor and control processes in Linux.',
        'prerequisites': ['basic-commands'],
        'content': [
            {
                'type': 'explanation',
                'title': 'Understanding Processes',
                'text': '''A process is a running instance of a program. Linux is a multi-tasking 
system that can run many processes simultaneously. Key concepts:
- PID: Process ID (unique identifier)
- Parent/Child processes
- Foreground vs Background processes
- Process states: running, sleeping, stopped, zombie'''
            },
            {
                'type': 'exercise',
                'title': 'Process Monitoring',
                'instructions': 'Learn to view and manage processes:',
                'commands': [
                    {'cmd': 'ps', 'description': 'Show processes for current user'},
                    {'cmd': 'ps aux', 'description': 'Show all processes with details'},
                    {'cmd': 'top', 'description': 'Real-time process viewer (press q to quit)'},
                    {'cmd': 'htop', 'description': 'Enhanced process viewer (if available)'},
                    {'cmd': 'pgrep python', 'description': 'Find process IDs by name'},
                    {'cmd': 'jobs', 'description': 'Show background jobs'}
                ]
            }
        ],
        'quiz': [
            {
                'type': 'fill_blank',
                'question': 'A _____ is a running instance of a program.',
                'answer': 'process',
                'explanation': 'A process is a running instance of a program with its own memory space and resources.'
            },
            {
                'type': 'fill_blank',
                'question': 'Every process has a unique identifier called a _____.',
                'answer': 'PID',
                'alternatives': ['Process ID', 'process ID', 'process id'],
                'explanation': 'PID (Process ID) is a unique number assigned to each process.'
            },
            {
                'type': 'command_recall',
                'question': 'Which command shows currently running processes?',
                'answer': 'ps',
                'alternatives': ['top', 'htop'],
                'explanation': 'ps displays process status. top and htop are also valid for viewing processes.'
            },
            {
                'type': 'multiple_choice',
                'question': 'What does "ps aux" show?',
                'options': [
                    'All processes from all users with detailed information',
                    'Only your processes',
                    'Only system processes',
                    'Available user accounts'
                ],
                'correct': 0,
                'explanation': '"ps aux" shows all processes (a=all users, u=user-oriented, x=include without tty).'
            },
            {
                'type': 'command_recall',
                'question': 'Which command provides real-time process monitoring?',
                'answer': 'top',
                'alternatives': ['htop'],
                'explanation': 'top provides real-time, dynamic view of running processes. htop is an enhanced alternative.'
            },
            {
                'type': 'true_false',
                'question': 'Each process can have child processes.',
                'answer': True,
                'explanation': 'True. Processes form a hierarchy where parent processes can spawn child processes.'
            },
            {
                'type': 'multiple_choice',
                'question': 'What are the typical process states in Linux?',
                'options': [
                    'Running, sleeping, stopped, zombie',
                    'Active, inactive, pending',
                    'Start, running, end',
                    'New, ready, terminated'
                ],
                'correct': 0,
                'explanation': 'Linux processes can be running, sleeping (waiting), stopped (paused), or zombie (terminated but not reaped).'
            },
            {
                'type': 'command_recall',
                'question': 'Which command finds process IDs by name?',
                'answer': 'pgrep',
                'alternatives': ['pidof'],
                'explanation': 'pgrep searches for processes by name and returns their PIDs. pidof also works for some cases.'
            },
            {
                'type': 'true_false',
                'question': 'Foreground processes block the terminal until they complete.',
                'answer': True,
                'explanation': 'True. Foreground processes occupy the terminal, while background processes run without blocking it.'
            },
            {
                'type': 'fill_blank',
                'question': 'A zombie process is one that has terminated but whose parent has not yet read its _____ code.',
                'answer': 'exit',
                'explanation': 'Zombie processes remain in the process table until the parent reads their exit status.'
            }
        ]
    },
    
    'shell-scripting': {
        'title': 'Introduction to Shell Scripting',
        'level': 'advanced',
        'duration': 45,
        'description': 'Learn to write powerful shell scripts to automate tasks.',
        'prerequisites': ['process-management', 'text-processing'],
        'content': [
            {
                'type': 'explanation',
                'title': 'What is Shell Scripting?',
                'text': '''Shell scripting allows you to combine multiple commands into a single file 
that can be executed. This is powerful for automation, system administration, and 
repetitive tasks. Key concepts:
- Shebang line (#!/bin/bash)
- Variables and parameter expansion
- Control structures (if, for, while)
- Functions and exit codes'''
            },
            {
                'type': 'exercise',
                'title': 'Your First Shell Script',
                'instructions': 'Create and run a simple shell script:',
                'commands': [
                    {'cmd': 'echo "#!/bin/bash" > myscript.sh', 'description': 'Create script with shebang'},
                    {'cmd': 'echo "echo \\"Hello from script!\\"" >> myscript.sh', 'description': 'Add command to script'},
                    {'cmd': 'chmod +x myscript.sh', 'description': 'Make script executable'},
                    {'cmd': 'cat myscript.sh', 'description': 'View script contents'},
                    {'cmd': './myscript.sh', 'description': 'Execute the script'}
                ]
            }
        ],
        'quiz': [
            {
                'type': 'fill_blank',
                'question': 'The first line of a shell script should be the _____ line.',
                'answer': 'shebang',
                'explanation': 'The shebang line (#!/bin/bash) tells the system which interpreter to use.'
            },
            {
                'type': 'multiple_choice',
                'question': 'What does #!/bin/bash at the start of a script do?',
                'options': [
                    'Specifies that the script should be run with bash',
                    'Makes the script executable',
                    'Comments out the first line',
                    'Imports bash functions'
                ],
                'correct': 0,
                'explanation': 'The shebang (#!/bin/bash) tells the system to execute the script using the bash shell.'
            },
            {
                'type': 'command_recall',
                'question': 'Which command makes a script file executable?',
                'answer': 'chmod +x',
                'alternatives': ['chmod u+x'],
                'explanation': 'chmod +x adds execute permission to make the script runnable.'
            },
            {
                'type': 'true_false',
                'question': 'Variables in bash are declared using the $ symbol.',
                'answer': False,
                'explanation': 'False. Variables are declared without $. The $ is used to access/expand variables (e.g., name="value", echo $name).'
            },
            {
                'type': 'multiple_choice',
                'question': 'How do you access the value of a variable named "count"?',
                'options': [
                    '$count',
                    'count',
                    '&count',
                    '@count'
                ],
                'correct': 0,
                'explanation': 'Use $variable_name to access variable values in bash scripts.'
            },
            {
                'type': 'fill_blank',
                'question': 'The _____ code indicates whether a command succeeded or failed.',
                'answer': 'exit',
                'alternatives': ['return', 'status'],
                'explanation': 'Exit codes (or return codes) indicate command success (0) or failure (non-zero).'
            },
            {
                'type': 'true_false',
                'question': 'An exit code of 0 typically means success.',
                'answer': True,
                'explanation': 'True. In Unix/Linux, exit code 0 indicates success, while non-zero indicates errors.'
            },
            {
                'type': 'multiple_choice',
                'question': 'Which control structure would you use to repeat commands?',
                'options': [
                    'for or while loops',
                    'if statements',
                    'case statements',
                    'functions'
                ],
                'correct': 0,
                'explanation': 'Loops (for, while, until) are used to repeat commands in shell scripts.'
            },
            {
                'type': 'command_recall',
                'question': 'How do you execute a script in the current directory named "script.sh"?',
                'answer': './script.sh',
                'alternatives': ['bash script.sh', 'sh script.sh'],
                'explanation': './script.sh runs the script directly. You can also use "bash script.sh" or "sh script.sh".'
            },
            {
                'type': 'true_false',
                'question': 'Shell scripts are useful for automating repetitive tasks.',
                'answer': True,
                'explanation': 'True. Shell scripts excel at automating system administration tasks and command sequences.'
            }
        ]
    },
    
    'security-basics': {
        'title': 'Linux Security Fundamentals',
        'level': 'advanced',
        'duration': 40,
        'description': 'Learn essential Linux security concepts and best practices.',
        'prerequisites': ['file-permissions', 'system-administration'],
        'content': [
            {
                'type': 'explanation',
                'title': 'Linux Security Concepts',
                'text': '''Linux security is built on several key principles:
- User and group permissions
- Principle of least privilege
- File system security (permissions, ACLs)
- Network security basics
- System updates and patch management
- Log monitoring and intrusion detection'''
            },
            {
                'type': 'exercise',
                'title': 'Security Assessment Commands',
                'instructions': 'Learn to assess system security:',
                'commands': [
                    {'cmd': 'id', 'description': 'Show current user and group information'},
                    {'cmd': 'sudo -l', 'description': 'List sudo privileges (if available)'},
                    {'cmd': 'find / -perm -4000 2>/dev/null', 'description': 'Find setuid files'},
                    {'cmd': 'netstat -tulpn', 'description': 'Show listening network services'},
                    {'cmd': 'ss -tulpn', 'description': 'Modern alternative to netstat'},
                    {'cmd': 'last', 'description': 'Show recent login history'}
                ]
            }
        ],
        'quiz': [
            {
                'type': 'multiple_choice',
                'question': 'What is the principle of least privilege?',
                'options': [
                    'Users should have only the minimum permissions needed',
                    'Only administrators should have privileges',
                    'All users should have equal privileges',
                    'Privileges should be granted generously'
                ],
                'correct': 0,
                'explanation': 'Least privilege means granting only the minimum permissions necessary for users to perform their tasks.'
            },
            {
                'type': 'true_false',
                'question': 'Setuid files can pose security risks if not properly managed.',
                'answer': True,
                'explanation': 'True. Setuid files run with the permissions of the file owner, which can be exploited if misconfigured.'
            },
            {
                'type': 'command_recall',
                'question': 'Which command shows your current user and group memberships?',
                'answer': 'id',
                'explanation': 'The id command displays user ID, group ID, and all group memberships.'
            },
            {
                'type': 'multiple_choice',
                'question': 'What does a setuid bit (4000 permission) do?',
                'options': [
                    'Allows file to execute with owner\'s privileges',
                    'Makes file read-only',
                    'Hides the file from listing',
                    'Encrypts the file contents'
                ],
                'correct': 0,
                'explanation': 'Setuid (4000) allows a file to execute with the privileges of its owner, not the user running it.'
            },
            {
                'type': 'command_recall',
                'question': 'Which command shows listening network services?',
                'answer': 'netstat -tulpn',
                'alternatives': ['ss -tulpn', 'ss', 'netstat'],
                'explanation': 'netstat -tulpn or ss -tulpn show listening TCP/UDP ports with program names.'
            },
            {
                'type': 'true_false',
                'question': 'Regular system updates are important for security.',
                'answer': True,
                'explanation': 'True. Updates patch security vulnerabilities and are essential for maintaining system security.'
            },
            {
                'type': 'fill_blank',
                'question': 'The _____ command shows recent login history.',
                'answer': 'last',
                'explanation': 'The last command displays login history from system logs.'
            },
            {
                'type': 'multiple_choice',
                'question': 'Why is log monitoring important for security?',
                'options': [
                    'It helps detect unauthorized access and security incidents',
                    'It speeds up the system',
                    'It reduces disk space',
                    'It automatically fixes vulnerabilities'
                ],
                'correct': 0,
                'explanation': 'Log monitoring helps identify suspicious activity, intrusion attempts, and security breaches.'
            },
            {
                'type': 'true_false',
                'question': 'File permissions are the only security mechanism in Linux.',
                'answer': False,
                'explanation': 'False. Linux security includes permissions, SELinux/AppArmor, firewalls, encryption, and many other mechanisms.'
            },
            {
                'type': 'multiple_choice',
                'question': 'What is the purpose of sudo?',
                'options': [
                    'Allow authorized users to run commands as root',
                    'Create new user accounts',
                    'Monitor system performance',
                    'Scan for viruses'
                ],
                'correct': 0,
                'explanation': 'sudo (superuser do) allows permitted users to execute commands with elevated (typically root) privileges.'
            }
        ]
    },
    
    'performance-tuning': {
        'title': 'Linux Performance Tuning',
        'level': 'expert',
        'duration': 60,
        'description': 'Advanced techniques for optimizing Linux system performance.',
        'prerequisites': ['process-management', 'system-administration'],
        'content': [
            {
                'type': 'explanation',
                'title': 'Performance Analysis Methodology',
                'text': '''Performance tuning requires systematic analysis:
1. Define performance goals and metrics
2. Establish baseline measurements
3. Identify bottlenecks (CPU, Memory, I/O, Network)
4. Apply targeted optimizations
5. Measure and validate improvements
6. Monitor for regressions'''
            },
            {
                'type': 'exercise',
                'title': 'Performance Monitoring Tools',
                'instructions': 'Master essential performance analysis tools:',
                'commands': [
                    {'cmd': 'uptime', 'description': 'System load average'},
                    {'cmd': 'free -h', 'description': 'Memory usage summary'},
                    {'cmd': 'df -h', 'description': 'Disk space usage'},
                    {'cmd': 'iostat -x 1 5', 'description': 'I/O statistics (if available)'},
                    {'cmd': 'vmstat 1 5', 'description': 'Virtual memory statistics'},
                    {'cmd': 'sar -u 1 5', 'description': 'CPU utilization over time (if available)'}
                ]
            }
        ],
        'quiz': [
            {
                'type': 'multiple_choice',
                'question': 'What are the four main system resource bottlenecks?',
                'options': [
                    'CPU, Memory, I/O, Network',
                    'Disk, RAM, Cache, Swap',
                    'Processes, Threads, Files, Sockets',
                    'Hardware, Software, Network, Users'
                ],
                'correct': 0,
                'explanation': 'The four main bottleneck areas are CPU, Memory (RAM), I/O (disk), and Network.'
            },
            {
                'type': 'command_recall',
                'question': 'Which command shows system load average?',
                'answer': 'uptime',
                'alternatives': ['w', 'top'],
                'explanation': 'uptime displays system load averages. Commands like w and top also show this information.'
            },
            {
                'type': 'command_recall',
                'question': 'Which command displays memory usage in human-readable format?',
                'answer': 'free -h',
                'explanation': 'free -h shows memory usage with human-readable units (MB, GB).'
            },
            {
                'type': 'true_false',
                'question': 'Performance tuning should always start with measuring baseline performance.',
                'answer': True,
                'explanation': 'True. You need baseline measurements to determine if optimizations actually improve performance.'
            },
            {
                'type': 'multiple_choice',
                'question': 'What does the load average represent?',
                'options': [
                    'Average number of processes in runnable or waiting state',
                    'CPU temperature over time',
                    'Network bandwidth usage',
                    'Disk space available'
                ],
                'correct': 0,
                'explanation': 'Load average shows the average number of processes running or waiting for CPU time.'
            },
            {
                'type': 'command_recall',
                'question': 'Which command shows disk space usage?',
                'answer': 'df -h',
                'alternatives': ['df'],
                'explanation': 'df -h displays disk space usage in human-readable format for all mounted filesystems.'
            },
            {
                'type': 'fill_blank',
                'question': 'The _____ command provides I/O statistics for block devices.',
                'answer': 'iostat',
                'explanation': 'iostat reports CPU statistics and I/O statistics for devices and partitions.'
            },
            {
                'type': 'true_false',
                'question': 'vmstat provides information about virtual memory and system activity.',
                'answer': True,
                'explanation': 'True. vmstat reports virtual memory statistics including processes, memory, paging, I/O, and CPU.'
            },
            {
                'type': 'multiple_choice',
                'question': 'What should you do after applying performance optimizations?',
                'options': [
                    'Measure and validate the improvements',
                    'Immediately apply more optimizations',
                    'Restart the system',
                    'Delete the baseline measurements'
                ],
                'correct': 0,
                'explanation': 'Always measure after optimizations to verify improvements and ensure you didn\'t introduce regressions.'
            },
            {
                'type': 'true_false',
                'question': 'You should optimize all parts of the system simultaneously for best results.',
                'answer': False,
                'explanation': 'False. Apply targeted optimizations one at a time so you can measure their individual impact.'
            }
        ]
    },

    'file-permissions': {
        'title': 'Understanding File Permissions',
        'level': 'beginner',
        'duration': 20,
        'description': 'Master Linux file permissions, ownership, and access control.',
        'prerequisites': ['basic-commands'],
        'content': [
            {
                'type': 'explanation',
                'title': 'Unix Permission Model',
                'text': '''Linux uses a permission system with three types of users:
- Owner (u): The file creator
- Group (g): Users in the file's group
- Others (o): Everyone else

Three permission types:
- Read (r/4): View file contents or list directory
- Write (w/2): Modify file or directory contents
- Execute (x/1): Run file as program or enter directory

Example: rwxr-xr-- means:
- Owner: read, write, execute (7)
- Group: read, execute (5)
- Others: read only (4)'''
            },
            {
                'type': 'exercise',
                'title': 'Viewing and Understanding Permissions',
                'instructions': 'Learn to read file permissions:',
                'commands': [
                    {'cmd': 'ls -l', 'description': 'List files with permissions'},
                    {'cmd': 'ls -la', 'description': 'Include hidden files'},
                    {'cmd': 'stat .bashrc', 'description': 'Detailed file information'},
                    {'cmd': 'ls -ld /tmp', 'description': 'Check directory permissions'}
                ]
            },
            {
                'type': 'explanation',
                'title': 'Changing Permissions',
                'text': '''Use chmod to modify permissions:

Symbolic method:
- chmod u+x file   # Add execute for owner
- chmod g-w file   # Remove write for group
- chmod o=r file   # Set others to read-only
- chmod a+r file   # Add read for all (a=all)

Numeric method (octal):
- chmod 755 file   # rwxr-xr-x
- chmod 644 file   # rw-r--r--
- chmod 600 file   # rw------- (private)'''
            },
            {
                'type': 'exercise',
                'title': 'Modifying Permissions',
                'instructions': 'Practice changing file permissions:',
                'commands': [
                    {'cmd': 'touch testfile.txt', 'description': 'Create test file'},
                    {'cmd': 'chmod 644 testfile.txt', 'description': 'Set to rw-r--r--'},
                    {'cmd': 'chmod u+x testfile.txt', 'description': 'Add execute for owner'},
                    {'cmd': 'chmod go-r testfile.txt', 'description': 'Remove read from group/others'},
                    {'cmd': 'ls -l testfile.txt', 'description': 'Verify new permissions'}
                ]
            },
            {
                'type': 'explanation',
                'title': 'File Ownership',
                'text': '''Every file has an owner and group:

Change ownership (requires sudo):
- chown user file        # Change owner
- chown user:group file  # Change owner and group
- chgrp group file       # Change group only

Check ownership:
- ls -l shows owner and group
- Use 'id' to see your user and groups'''
            },
            {
                'type': 'exercise',
                'title': 'Working with Ownership',
                'instructions': 'Understand file ownership:',
                'commands': [
                    {'cmd': 'id', 'description': 'Show your user ID and groups'},
                    {'cmd': 'ls -l testfile.txt', 'description': 'See file owner and group'},
                    {'cmd': 'groups', 'description': 'List your groups'},
                    {'cmd': 'stat testfile.txt', 'description': 'Detailed ownership info'}
                ]
            }
        ],
        'quiz': [
            {
                'type': 'multiple_choice',
                'question': 'How many permission categories exist in Linux?',
                'options': [
                    'Three: owner, group, others',
                    'Two: user and admin',
                    'Four: read, write, execute, delete',
                    'One: user permissions'
                ],
                'correct': 0,
                'explanation': 'Linux has three permission categories: owner (u), group (g), and others (o).'
            },
            {
                'type': 'multiple_choice',
                'question': 'What are the three basic permission types?',
                'options': [
                    'Read, write, execute',
                    'Create, modify, delete',
                    'View, edit, run',
                    'Open, save, close'
                ],
                'correct': 0,
                'explanation': 'The three permission types are read (r), write (w), and execute (x).'
            },
            {
                'type': 'fill_blank',
                'question': 'The _____ command changes file permissions.',
                'answer': 'chmod',
                'explanation': 'chmod (change mode) modifies file permissions.'
            },
            {
                'type': 'multiple_choice',
                'question': 'What does "chmod 755 file" mean?',
                'options': [
                    'Owner: rwx, Group: r-x, Others: r-x',
                    'Owner: r-x, Group: rwx, Others: r-x',
                    'Owner: rwx, Group: rwx, Others: rwx',
                    'Owner: r--, Group: r--, Others: r--'
                ],
                'correct': 0,
                'explanation': '755 = rwxr-xr-x (7=rwx for owner, 5=r-x for group and others).'
            },
            {
                'type': 'command_recall',
                'question': 'Which command changes file ownership?',
                'answer': 'chown',
                'explanation': 'chown (change owner) modifies file ownership.'
            },
            {
                'type': 'true_false',
                'question': 'The read permission (r) has a numeric value of 4.',
                'answer': True,
                'explanation': 'True. Permission values are: read=4, write=2, execute=1.'
            },
            {
                'type': 'multiple_choice',
                'question': 'What does "chmod u+x file" do?',
                'options': [
                    'Adds execute permission for the owner',
                    'Removes execute permission for the owner',
                    'Adds execute permission for everyone',
                    'Changes the user ownership'
                ],
                'correct': 0,
                'explanation': 'u+x adds (+) execute (x) permission for the user/owner (u).'
            },
            {
                'type': 'fill_blank',
                'question': 'In permissions, "w" stands for _____.',
                'answer': 'write',
                'explanation': 'The "w" permission allows write/modify access to files or directories.'
            },
            {
                'type': 'true_false',
                'question': 'The execute permission on a directory allows you to enter it.',
                'answer': True,
                'explanation': 'True. Execute (x) permission on directories allows you to cd into them.'
            },
            {
                'type': 'multiple_choice',
                'question': 'What does "chmod 600 file" do?',
                'options': [
                    'Makes the file private to owner (rw-------)',
                    'Gives everyone read access',
                    'Makes the file read-only',
                    'Removes all permissions'
                ],
                'correct': 0,
                'explanation': '600 = rw------- (owner can read/write, no permissions for group/others).'
            }
        ]
    },

    'text-editors': {
        'title': 'Working with Text Editors',
        'level': 'beginner',
        'duration': 25,
        'description': 'Learn essential text editors: nano, vim basics, and when to use each.',
        'prerequisites': ['basic-commands'],
        'content': [
            {
                'type': 'explanation',
                'title': 'Why Text Editors Matter',
                'text': '''In Linux, you'll frequently edit configuration files, scripts, and code.
Common text editors:
- nano: Beginner-friendly, simple interface
- vim/vi: Powerful, modal editor (learning curve)
- emacs: Extensible, feature-rich (advanced)
- gedit/kate: GUI editors (if available)

We'll focus on nano (easy) and vim basics (essential).'''
            },
            {
                'type': 'exercise',
                'title': 'Nano - The Friendly Editor',
                'instructions': 'Learn nano basics:',
                'commands': [
                    {'cmd': 'nano', 'description': 'Open nano editor (Ctrl+X to exit)'},
                    {'cmd': 'nano filename.txt', 'description': 'Create/edit a file'},
                    {'cmd': 'nano -l filename.txt', 'description': 'Open with line numbers'},
                    {'cmd': 'cat filename.txt', 'description': 'View what you created'}
                ]
            },
            {
                'type': 'explanation',
                'title': 'Nano Shortcuts',
                'text': '''Essential nano commands (^ means Ctrl):
- ^X: Exit (prompts to save)
- ^O: Save file (write Out)
- ^W: Search (Where is)
- ^K: Cut line
- ^U: Paste (uncut)
- ^G: Get help (shows all shortcuts)

Bottom of screen shows available commands.'''
            },
            {
                'type': 'explanation',
                'title': 'Vim Basics - Survival Guide',
                'text': '''Vim is everywhere in Linux. Learn these basics:

Vim has modes:
- Normal mode: Navigate and command (default)
- Insert mode: Type text (press 'i' to enter)
- Command mode: Execute commands (press ':')

Absolute minimum to survive:
- i: Enter insert mode (type text)
- Esc: Return to normal mode
- :w: Write (save) file
- :q: Quit vim
- :wq: Save and quit
- :q!: Quit without saving (force)'''
            },
            {
                'type': 'exercise',
                'title': 'Vim Practice (Safe)',
                'instructions': 'Try vim commands (we\'ll guide you):',
                'commands': [
                    {'cmd': 'vimtutor', 'description': 'Interactive vim tutorial (recommended!)'},
                    {'cmd': 'vim', 'description': 'Open vim (type :q! to exit)'},
                    {'cmd': 'vim testfile.txt', 'description': 'Edit file in vim'}
                ]
            },
            {
                'type': 'explanation',
                'title': 'Which Editor When?',
                'text': '''Choose your editor:

Use nano when:
- Quick edits
- You're new to Linux
- Simple configuration changes
- The instructions say so

Use vim when:
- Already on a system without nano
- Want powerful features
- Editing code/scripts
- Faster navigation (with practice)

Pro tip: Start with nano, learn vim gradually. Many sysadmins know both!'''
            }
        ],
        'quiz': [
            {
                'type': 'multiple_choice',
                'question': 'Which text editor is most beginner-friendly?',
                'options': [
                    'nano',
                    'vim',
                    'emacs',
                    'ed'
                ],
                'correct': 0,
                'explanation': 'nano is the most beginner-friendly with an intuitive interface and on-screen help.'
            },
            {
                'type': 'fill_blank',
                'question': 'In nano, press _____ to exit the editor.',
                'answer': 'Ctrl+X',
                'alternatives': ['^X', 'Control+X'],
                'explanation': 'Ctrl+X (or ^X) exits nano, prompting to save if there are changes.'
            },
            {
                'type': 'true_false',
                'question': 'Vim has different modes for editing and navigating.',
                'answer': True,
                'explanation': 'True. Vim is a modal editor with Normal mode, Insert mode, and Command mode.'
            },
            {
                'type': 'multiple_choice',
                'question': 'How do you enter insert mode in vim?',
                'options': [
                    'Press i',
                    'Press Ctrl+I',
                    'Type :insert',
                    'Press Enter'
                ],
                'correct': 0,
                'explanation': 'Press "i" to enter Insert mode in vim, allowing you to type text.'
            },
            {
                'type': 'command_recall',
                'question': 'What vim command saves and quits?',
                'answer': ':wq',
                'alternatives': [':x', 'ZZ'],
                'explanation': ':wq writes (saves) and quits. :x and ZZ also work.'
            },
            {
                'type': 'fill_blank',
                'question': 'In nano, _____ means Ctrl (as in ^X means Ctrl+X).',
                'answer': '^',
                'alternatives': ['caret'],
                'explanation': 'The caret symbol (^) represents the Ctrl key in nano documentation.'
            },
            {
                'type': 'multiple_choice',
                'question': 'How do you quit vim without saving changes?',
                'options': [
                    ':q!',
                    ':quit',
                    ':exit',
                    ':q'
                ],
                'correct': 0,
                'explanation': ':q! force-quits vim without saving (! means force).'
            },
            {
                'type': 'true_false',
                'question': 'In nano, Ctrl+O saves the file.',
                'answer': True,
                'explanation': 'True. Ctrl+O (write Out) saves the file in nano.'
            },
            {
                'type': 'multiple_choice',
                'question': 'What is vimtutor?',
                'options': [
                    'An interactive tutorial for learning vim',
                    'A vim plugin manager',
                    'A vim configuration file',
                    'A vim documentation viewer'
                ],
                'correct': 0,
                'explanation': 'vimtutor is an interactive tutorial that teaches vim basics step-by-step.'
            },
            {
                'type': 'command_recall',
                'question': 'Which key returns you to normal mode in vim?',
                'answer': 'Esc',
                'alternatives': ['Escape'],
                'explanation': 'Esc (Escape) returns you to Normal mode from any other vim mode.'
            }
        ]
    }
}

def get_lesson(lesson_name: str) -> Optional[Dict[str, Any]]:
    return LESSONS.get(lesson_name)

def run_lesson(lesson: Dict[str, Any], tutor) -> None:
    """Run a lesson interactively with quiz at the end."""
    # Get lesson ID by finding it in LESSONS dict
    lesson_id = None
    for lid, ldata in LESSONS.items():
        if ldata is lesson:
            lesson_id = lid
            break

    print(f"\n{'='*50}")
    print(f"Starting: {lesson['title']}")
    print(f"{'='*50}\n")

    # Track simulated file system state for this lesson
    simulated_fs = {
        'directories': set(),
        'files': {},  # filename -> content
    }

    for i, section in enumerate(lesson['content'], 1):
        print(f"\n--- Section {i}: {section['title']} ---\n")

        if section['type'] == 'explanation':
            print(section['text'])
            input("\nPress Enter to continue...")

        elif section['type'] == 'exercise':
            print(section['text'] if 'text' in section else section['instructions'])
            print()

            for cmd_info in section['commands']:
                print(f"Command: {cmd_info['cmd']}")
                print(f"Purpose: {cmd_info['description']}")

                choice = input("\n[r]un, [s]kip, or [q]uit? ").lower().strip()

                if choice == 'q':
                    print("Lesson interrupted.")
                    return
                elif choice == 's':
                    print("Skipped.")
                    continue
                elif choice == 'r' or choice == '':
                    try:
                        print(f"\n$ {cmd_info['cmd']}")

                        # Parse command
                        cmd_parts = cmd_info['cmd'].split()
                        cmd = cmd_parts[0]

                        # Handle different commands
                        if cmd in ['whoami', 'pwd', 'date', 'uname']:
                            # These are safe to run directly
                            result = subprocess.run(cmd_info['cmd'], shell=True,
                                                 capture_output=True, text=True)
                            if result.returncode == 0:
                                print(result.stdout)
                            else:
                                print(f"Error: {result.stderr}")

                        elif cmd == 'mkdir':
                            # Simulate directory creation
                            if len(cmd_parts) > 1:
                                dirname = cmd_parts[1]
                                simulated_fs['directories'].add(dirname)
                                print(f"[SIMULATION] Created directory: {dirname}")
                            else:
                                print("[SIMULATION] This command would create a directory")

                        elif cmd == 'touch':
                            # Simulate file creation
                            if len(cmd_parts) > 1:
                                filename = cmd_parts[1]
                                simulated_fs['files'][filename] = ""
                                print(f"[SIMULATION] Created empty file: {filename}")
                            else:
                                print("[SIMULATION] This command would create an empty file")

                        elif cmd == 'echo' and '>' in cmd_info['cmd']:
                            # Simulate file writing
                            parts = cmd_info['cmd'].split('>')
                            if len(parts) == 2:
                                content = parts[0].split('echo')[1].strip().strip('"\'')
                                filename = parts[1].strip()
                                simulated_fs['files'][filename] = content
                                print(f"[SIMULATION] Wrote '{content}' to {filename}")
                            else:
                                print("[SIMULATION] This command would write to a file")

                        elif cmd == 'cat':
                            # Simulate file reading
                            if len(cmd_parts) > 1:
                                filename = cmd_parts[1]
                                if filename in simulated_fs['files']:
                                    content = simulated_fs['files'][filename]
                                    print(content if content else f"[SIMULATION] {filename} is empty")
                                else:
                                    print(f"[SIMULATION] File {filename} not found (would show error)")
                            else:
                                print("[SIMULATION] This command would display file contents")

                        elif cmd == 'cp':
                            # Simulate file copying
                            if len(cmd_parts) >= 3:
                                src = cmd_parts[1]
                                dst = cmd_parts[2]
                                if src in simulated_fs['files']:
                                    simulated_fs['files'][dst] = simulated_fs['files'][src]
                                    print(f"[SIMULATION] Copied {src} to {dst}")
                                else:
                                    print(f"[SIMULATION] Would copy {src} to {dst}")
                            else:
                                print("[SIMULATION] This command would copy a file")

                        elif cmd == 'mv':
                            # Simulate file moving
                            if len(cmd_parts) >= 3:
                                src = cmd_parts[1]
                                dst = cmd_parts[2]
                                if dst.endswith('/'):
                                    # Moving to directory
                                    dirname = dst.rstrip('/')
                                    if dirname in simulated_fs['directories']:
                                        if src in simulated_fs['files']:
                                            new_path = f"{dirname}/{src}"
                                            simulated_fs['files'][new_path] = simulated_fs['files'][src]
                                            del simulated_fs['files'][src]
                                            print(f"[SIMULATION] Moved {src} to {dirname}/")
                                        else:
                                            print(f"[SIMULATION] Would move {src} to {dirname}/")
                                    else:
                                        print(f"[SIMULATION] Directory {dirname} doesn't exist")
                                else:
                                    print(f"[SIMULATION] Would move/rename {src} to {dst}")
                            else:
                                print("[SIMULATION] This command would move/rename a file")

                        elif cmd == 'ls':
                            # Simulate directory listing
                            if len(cmd_parts) > 1:
                                target = cmd_parts[1].rstrip('/')
                                if target in simulated_fs['directories']:
                                    # List files in the directory
                                    files_in_dir = [f.split('/')[-1] for f in simulated_fs['files'].keys()
                                                  if f.startswith(f"{target}/")]
                                    if files_in_dir:
                                        print('\n'.join(files_in_dir))
                                    else:
                                        print(f"[SIMULATION] Directory {target}/ is empty")
                                else:
                                    print(f"[SIMULATION] Directory {target} doesn't exist")
                            else:
                                # List current directory - show simulated files
                                current_files = [f for f in simulated_fs['files'].keys() if '/' not in f]
                                current_dirs = list(simulated_fs['directories'])
                                all_items = current_dirs + current_files
                                if all_items:
                                    print('\n'.join(all_items))
                                else:
                                    print("[SIMULATION] Current directory appears empty")

                        else:
                            print(f"[SIMULATION] This command would execute: {cmd_info['cmd']}")
                            print("(In a real environment, you would run this command)")

                    except Exception as e:
                        print(f"Error running command: {e}")

                print("-" * 40)

    # After all sections complete, run quiz if available
    quiz_data = lesson.get('quiz')
    if quiz_data:
        print("\n" + "="*50)
        print("Lesson Complete!")
        print("="*50)

        # Ask if ready for quiz
        if not prompt_yes_no("\nReady to start the quiz? [Y/n]: "):
            print("\nYou can come back to complete the quiz later.")
            print("The lesson won't be marked complete until you pass the quiz.")
            return

        # Run quiz
        quiz = Quiz(quiz_data)
        runner = QuizRunner(quiz)
        attempts, completed = runner.run()

        # Update progress with quiz stats only if completed
        if completed:
            tutor.progress = tutor.progress_mgr.increment_quiz_stats(tutor.progress, attempts)
            tutor.save_progress()

            # Mark lesson complete only if quiz was completed
            if lesson_id:
                tutor.complete_lesson(lesson_id)
                tutor.progress['stats']['exercises_completed'] += len([s for s in lesson['content'] if s['type'] == 'exercise'])
                tutor.save_progress()
        else:
            print("\nQuiz not completed. You can retry this lesson later to complete the quiz.")
            return
    else:
        # No quiz for this lesson - mark as complete
        print("\n" + "="*50)
        print("Lesson Complete!")
        print("="*50)

        if lesson_id:
            tutor.complete_lesson(lesson_id)
            tutor.progress['stats']['exercises_completed'] += len([s for s in lesson['content'] if s['type'] == 'exercise'])
            tutor.save_progress()

def list_all_lessons() -> Dict[str, List[str]]:
    levels = {}
    for lesson_name, lesson_data in LESSONS.items():
        level = lesson_data['level']
        if level not in levels:
            levels[level] = []
        levels[level].append(lesson_name)
    return levels

# Search functionality

def _extract_snippet(text: str, keyword: str, context_chars: int = 50) -> str:
    """
    Extract a snippet of text around the keyword for display.

    Args:
        text: The full text to extract from
        keyword: The keyword to find (case-insensitive)
        context_chars: Number of characters to show before and after keyword

    Returns:
        A snippet string with context around the keyword
    """
    text_lower = text.lower()
    keyword_lower = keyword.lower()

    pos = text_lower.find(keyword_lower)
    if pos == -1:
        return ""

    # Calculate start and end positions
    start = max(0, pos - context_chars)
    end = min(len(text), pos + len(keyword) + context_chars)

    # Extract snippet
    snippet = text[start:end]

    # Add ellipsis if truncated
    if start > 0:
        snippet = "..." + snippet
    if end < len(text):
        snippet = snippet + "..."

    return snippet

def _calculate_score(matches: Dict[str, int]) -> int:
    """
    Calculate relevance score based on match counts and field weights.

    Args:
        matches: Dictionary mapping field types to match counts

    Returns:
        Total weighted score
    """
    weights = {
        'title': 10,
        'description': 5,
        'section_title': 3,
        'command_desc': 2,
        'command': 2,
        'text': 1,
        'level': 3,
    }

    score = 0
    for field_type, count in matches.items():
        weight = weights.get(field_type, 1)
        score += count * weight

    return score

def _search_in_lesson(lesson_data: Dict, keywords: List[str]) -> Optional[Dict]:
    """
    Search a single lesson for all keywords.

    Args:
        lesson_data: The lesson dictionary to search
        keywords: List of keywords (case-insensitive, AND logic)

    Returns:
        Match info dict if ALL keywords found, None otherwise.
        Match info contains: matches, score, fields_matched, snippets
    """
    from collections import defaultdict

    keywords_lower = [k.lower() for k in keywords]
    matches = defaultdict(int)  # field_type -> count
    snippets = {}  # field_type -> snippet text
    fields_matched = set()

    # Track which keywords were found anywhere in the lesson
    keywords_found = set()

    # Search lesson title
    title_lower = lesson_data['title'].lower()
    for kw in keywords_lower:
        count = title_lower.count(kw)
        if count > 0:
            matches['title'] += count
            fields_matched.add('title')
            keywords_found.add(kw)

    # Search lesson description
    desc_lower = lesson_data['description'].lower()
    for kw in keywords_lower:
        count = desc_lower.count(kw)
        if count > 0:
            matches['description'] += count
            fields_matched.add('description')
            keywords_found.add(kw)
            # Extract snippet for first keyword match in description
            if 'description' not in snippets:
                snippets['description'] = _extract_snippet(lesson_data['description'], kw)

    # Search lesson level
    level_lower = lesson_data['level'].lower()
    for kw in keywords_lower:
        if kw in level_lower:
            matches['level'] += 1
            fields_matched.add('level')
            keywords_found.add(kw)

    # Search content sections
    for section in lesson_data.get('content', []):
        # Search section title
        section_title = section.get('title', '')
        section_title_lower = section_title.lower()
        for kw in keywords_lower:
            count = section_title_lower.count(kw)
            if count > 0:
                matches['section_title'] += count
                fields_matched.add('section_title')
                keywords_found.add(kw)
                if 'section_title' not in snippets:
                    snippets['section_title'] = _extract_snippet(section_title, kw)

        # Search explanation text
        if section.get('type') == 'explanation':
            text = section.get('text', '')
            text_lower = text.lower()
            for kw in keywords_lower:
                count = text_lower.count(kw)
                if count > 0:
                    matches['text'] += count
                    fields_matched.add('text')
                    keywords_found.add(kw)
                    if 'text' not in snippets:
                        snippets['text'] = _extract_snippet(text, kw)

        # Search exercise instructions
        if section.get('type') == 'exercise':
            instructions = section.get('instructions', '')
            instructions_lower = instructions.lower()
            for kw in keywords_lower:
                count = instructions_lower.count(kw)
                if count > 0:
                    matches['text'] += count
                    fields_matched.add('text')
                    keywords_found.add(kw)
                    if 'text' not in snippets and instructions:
                        snippets['text'] = _extract_snippet(instructions, kw)

            # Search commands
            for cmd_info in section.get('commands', []):
                # Search command itself
                cmd = cmd_info.get('cmd', '')
                cmd_lower = cmd.lower()
                for kw in keywords_lower:
                    count = cmd_lower.count(kw)
                    if count > 0:
                        matches['command'] += count
                        fields_matched.add('command')
                        keywords_found.add(kw)
                        if 'command' not in snippets:
                            snippets['command'] = _extract_snippet(cmd, kw)

                # Search command description
                cmd_desc = cmd_info.get('description', '')
                cmd_desc_lower = cmd_desc.lower()
                for kw in keywords_lower:
                    count = cmd_desc_lower.count(kw)
                    if count > 0:
                        matches['command_desc'] += count
                        fields_matched.add('command_desc')
                        keywords_found.add(kw)
                        if 'command_desc' not in snippets:
                            snippets['command_desc'] = _extract_snippet(cmd_desc, kw)

    # Check if ALL keywords were found (AND logic)
    if len(keywords_found) != len(keywords_lower):
        return None

    # Calculate score
    score = _calculate_score(matches)

    return {
        'matches': matches,
        'score': score,
        'fields_matched': fields_matched,
        'snippets': snippets
    }

def search_lessons(keywords: List[str]) -> List[Dict[str, Any]]:
    """
    Search all lessons for keywords with AND logic and relevance ranking.

    Args:
        keywords: List of search terms (case-insensitive, all must match)

    Returns:
        List of match result dicts, sorted by relevance (highest first).
        Each result contains:
        - lesson_id: Lesson identifier
        - lesson_data: Full lesson dictionary
        - score: Relevance score
        - fields_matched: Set of field types where keywords were found
        - snippets: Dict mapping field types to text snippets
    """
    results = []

    for lesson_id, lesson_data in LESSONS.items():
        match_info = _search_in_lesson(lesson_data, keywords)
        if match_info:
            results.append({
                'lesson_id': lesson_id,
                'lesson_data': lesson_data,
                'score': match_info['score'],
                'fields_matched': match_info['fields_matched'],
                'snippets': match_info['snippets']
            })

    # Sort by score (highest first)
    results.sort(key=lambda x: x['score'], reverse=True)

    return results