#!/usr/bin/env python3
"""
HIPE: File Versioning CLI
A Linux terminal tool for tracking file changes with easy version management.
"""

import os
import sys
import json
import shutil
from datetime import datetime
from pathlib import Path
from difflib import unified_diff

__version__ = "0.0.2"
VERSIONS_DIR = ".hipe_versions"


class HipeManager:
    """Manages file versioning operations."""
    
    def __init__(self):
        self.versions_dir = Path(VERSIONS_DIR)
    
    def _get_file_versions_dir(self, file_path):
        """Get the versions directory for a specific file."""
        file_name = Path(file_path).name
        return self.versions_dir / file_name.replace('.', '_')
    
    def _ensure_dirs(self):
        """Ensure necessary directories exist."""
        self.versions_dir.mkdir(exist_ok=True)
    
    def _load_metadata(self, file_path):
        """Load version metadata for a file."""
        file_versions_dir = self._get_file_versions_dir(file_path)
        metadata_file = file_versions_dir / "metadata.json"
        
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                return json.load(f)
        return {"versions": []}
    
    def _save_metadata(self, file_path, metadata):
        """Save version metadata for a file."""
        file_versions_dir = self._get_file_versions_dir(file_path)
        metadata_file = file_versions_dir / "metadata.json"
        
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def save(self, file_path):
        """Save a version of the specified file."""
        if not Path(file_path).exists():
            print(f"❌ Error: File '{file_path}' not found")
            return False
        
        self._ensure_dirs()
        
        file_versions_dir = self._get_file_versions_dir(file_path)
        file_versions_dir.mkdir(parents=True, exist_ok=True)
        
        metadata = self._load_metadata(file_path)
        version_num = len(metadata["versions"]) + 1
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        version_file = file_versions_dir / f"v{version_num}.txt"
        
        # Copy file content
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as src:
            content = src.read()
        
        with open(version_file, 'w', encoding='utf-8') as dst:
            dst.write(content)
        
        # Update metadata
        metadata["versions"].append({
            "version": version_num,
            "timestamp": timestamp,
            "file_size": len(content)
        })
        
        self._save_metadata(file_path, metadata)
        
        print(f"✅ Saved version {version_num} of '{file_path}' at {timestamp}")
        return True
    
    def history(self, file_path):
        """Display version history for a file."""
        file_versions_dir = self._get_file_versions_dir(file_path)
        
        if not file_versions_dir.exists():
            print(f"❌ No version history found for '{file_path}'")
            return
        
        metadata = self._load_metadata(file_path)
        
        if not metadata["versions"]:
            print(f"❌ No versions saved for '{file_path}'")
            return
        
        print(f"\n📜 Version history for '{file_path}':\n")
        for v in metadata["versions"]:
            print(f"   Version {v['version']} - {v['timestamp']} ({v['file_size']} bytes)")
        print()
    
    def restore(self, file_path, version_num):
        """Restore a file to a previous version."""
        try:
            version_num = int(version_num)
        except ValueError:
            print(f"❌ Error: Version number must be an integer")
            return False
        
        file_versions_dir = self._get_file_versions_dir(file_path)
        version_file = file_versions_dir / f"v{version_num}.txt"
        
        if not version_file.exists():
            print(f"❌ Error: Version {version_num} of '{file_path}' not found")
            return False
        
        # Read version content
        with open(version_file, 'r', encoding='utf-8') as src:
            content = src.read()
        
        # Write to original file
        with open(file_path, 'w', encoding='utf-8') as dst:
            dst.write(content)
        
        metadata = self._load_metadata(file_path)
        version_info = next((v for v in metadata["versions"] if v["version"] == version_num), None)
        
        if version_info:
            print(f"✅ Restored '{file_path}' to version {version_num} ({version_info['timestamp']})")
        else:
            print(f"✅ Restored '{file_path}' to version {version_num}")
        
        return True
    
    def diff(self, file_path, version_a, version_b):
        """Show differences between two versions."""
        try:
            version_a = int(version_a)
            version_b = int(version_b)
        except ValueError:
            print(f"❌ Error: Version numbers must be integers")
            return False
        
        file_versions_dir = self._get_file_versions_dir(file_path)
        version_file_a = file_versions_dir / f"v{version_a}.txt"
        version_file_b = file_versions_dir / f"v{version_b}.txt"
        
        if not version_file_a.exists():
            print(f"❌ Error: Version {version_a} of '{file_path}' not found")
            return False
        
        if not version_file_b.exists():
            print(f"❌ Error: Version {version_b} of '{file_path}' not found")
            return False
        
        with open(version_file_a, 'r', encoding='utf-8') as f:
            lines_a = f.readlines()
        
        with open(version_file_b, 'r', encoding='utf-8') as f:
            lines_b = f.readlines()
        
        diff_lines = list(unified_diff(lines_a, lines_b, fromfile=f"v{version_a}", tofile=f"v{version_b}"))
        
        if diff_lines:
            print(f"\n🆚 Differences between version {version_a} and {version_b} of '{file_path}':\n")
            for line in diff_lines:
                if line.startswith('+'):
                    print(f"  🟢 {line}", end='')
                elif line.startswith('-'):
                    print(f"  🔴 {line}", end='')
                else:
                    print(f"  {line}", end='')
            print()
        else:
            print(f"\n✅ No differences between version {version_a} and {version_b}")


def show_version():
    """Display version information."""
    print(f"HIPE v{__version__}")


def show_help():
    """Display help information."""
    help_text = f"""
HIPE v{__version__} - File Versioning CLI

Usage: hipe <command> [options]

Commands:
  save <file>           Save a version of the file
  history <file>        Show version history of a file
  restore <file> <v>    Restore file to version number
  diff <file> <v1> <v2> Compare two versions
  --version             Show version information
  --help                Show this help message

Examples:
  hipe save document.txt
  hipe history document.txt
  hipe restore document.txt 2
  hipe diff document.txt 1 3

Learn more: https://github.com/YusufEremK/hipe
"""
    print(help_text)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1]
    manager = HipeManager()
    
    if command == "--version":
        show_version()
    elif command == "--help":
        show_help()
    elif command == "save":
        if len(sys.argv) < 3:
            print("❌ Error: Please specify a file")
            return
        manager.save(sys.argv[2])
    elif command == "history":
        if len(sys.argv) < 3:
            print("❌ Error: Please specify a file")
            return
        manager.history(sys.argv[2])
    elif command == "restore":
        if len(sys.argv) < 4:
            print("❌ Error: Please specify file and version number")
            return
        manager.restore(sys.argv[2], sys.argv[3])
    elif command == "diff":
        if len(sys.argv) < 5:
            print("❌ Error: Please specify file and two version numbers")
            return
        manager.diff(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print(f"❌ Unknown command: {command}")
        show_help()


if __name__ == "__main__":
    main()
