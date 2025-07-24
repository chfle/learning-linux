#!/usr/bin/env python3

import os
import sys
import shutil
from pathlib import Path

def create_symlink():
    """Create a symlink to make linuxtutor available system-wide"""
    script_path = Path(__file__).parent / 'linuxtutor.py'
    local_bin = Path.home() / '.local' / 'bin'
    local_bin.mkdir(parents=True, exist_ok=True)
    
    symlink_path = local_bin / 'linuxtutor'
    
    if symlink_path.exists():
        symlink_path.unlink()
    
    try:
        symlink_path.symlink_to(script_path.absolute())
        print(f"✓ Created symlink: {symlink_path} -> {script_path}")
        return True
    except OSError as e:
        print(f"✗ Failed to create symlink: {e}")
        return False

def check_path():
    """Check if ~/.local/bin is in PATH"""
    local_bin = str(Path.home() / '.local' / 'bin')
    path_dirs = os.environ.get('PATH', '').split(':')
    
    if local_bin in path_dirs:
        print(f"✓ {local_bin} is in your PATH")
        return True
    else:
        print(f"✗ {local_bin} is not in your PATH")
        print("\nTo add it, run one of these commands:")
        print(f"  echo 'export PATH=\"$HOME/.local/bin:$PATH\"' >> ~/.bashrc")
        print(f"  echo 'export PATH=\"$HOME/.local/bin:$PATH\"' >> ~/.zshrc")
        print("\nThen restart your terminal or run: source ~/.bashrc")
        return False

def install():
    """Install LinuxTutor"""
    print("Installing LinuxTutor...")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 6):
        print("✗ Python 3.6+ required")
        return False
    
    print(f"✓ Python {sys.version.split()[0]} detected")
    
    # Create symlink
    if not create_symlink():
        return False
    
    # Check PATH
    path_ok = check_path()
    
    print("\n" + "=" * 40)
    print("Installation Summary:")
    print(f"✓ LinuxTutor files: {Path(__file__).parent}")
    print(f"✓ Executable link: ~/.local/bin/linuxtutor")
    
    if path_ok:
        print("\n🎉 Installation complete!")
        print("\nTry it out:")
        print("  linuxtutor help")
        print("  linuxtutor status")
        print("  linuxtutor lessons")
    else:
        print("\n⚠️  Installation complete, but PATH needs updating")
        print("   Follow the instructions above to add ~/.local/bin to PATH")
    
    return True

def uninstall():
    """Uninstall LinuxTutor"""
    print("Uninstalling LinuxTutor...")
    
    # Remove symlink
    symlink_path = Path.home() / '.local' / 'bin' / 'linuxtutor'
    if symlink_path.exists():
        symlink_path.unlink()
        print(f"✓ Removed: {symlink_path}")
    
    # Remove config directory
    config_dir = Path.home() / '.linuxtutor'
    if config_dir.exists():
        shutil.rmtree(config_dir)
        print(f"✓ Removed config directory: {config_dir}")
    
    print("✓ LinuxTutor uninstalled")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'uninstall':
        uninstall()
    else:
        install()

if __name__ == '__main__':
    main()