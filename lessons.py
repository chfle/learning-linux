import os
import sys
import subprocess
from typing import Dict, List, Optional, Any

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
        ]
    }
}

def get_lesson(lesson_name: str) -> Optional[Dict[str, Any]]:
    return LESSONS.get(lesson_name)

def run_lesson(lesson: Dict[str, Any], tutor) -> None:
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
    
    print(f"\n{'='*50}")
    print("Lesson completed! 🎉")
    print(f"{'='*50}")
    
    # Mark lesson as completed
    lesson_name = None
    for name, data in LESSONS.items():
        if data == lesson:
            lesson_name = name
            break
    
    if lesson_name:
        tutor.complete_lesson(lesson_name)
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