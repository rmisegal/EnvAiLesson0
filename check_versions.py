#!/usr/bin/env python3
"""
AI Environment Version Checker v3.0.0
Cross-platform Python version of check_versions.bat
Dynamically reads all files from version_config.json

Author: AI Environment Team
Date: 2025-08-12
Version: 3.0.0
"""

import json
import os
import sys

from version_utils import (
    Colors,
    check_files_category,
    print_summary,
    print_footer,
    set_last_status,
)

# Version information
SCRIPT_VERSION = "3.0.0"
SCRIPT_DATE = "2025-08-12"

def print_header():
    """Print the header banner"""
    print("================================================================")
    print("                   AI Environment Version Checker")
    print(f"                     Version {SCRIPT_VERSION} ({SCRIPT_DATE})")
    print("                     Python Cross-Platform Mode")
    print("================================================================")
    print()

def load_config():
    """Load the version configuration from JSON"""
    config_file = "version_config.json"
    
    print(f"[INFO] Checking file versions in: {os.getcwd()}")
    print(f"[INFO] Using configuration: {config_file}")
    print()
    
    try:
        if not os.path.exists(config_file):
            print(f"{Colors.RED}[ERROR] Configuration file not found: {config_file}{Colors.RESET}")
            return None
            
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            
        print(f"{Colors.GREEN}[OK] Configuration file found: {config_file}{Colors.RESET}")
        print()
        
        return config
        
    except json.JSONDecodeError as e:
        print(f"{Colors.RED}[ERROR] Invalid JSON in {config_file}: {e}{Colors.RESET}")
        return None
    except Exception as e:
        print(f"{Colors.RED}[ERROR] Failed to load {config_file}: {e}{Colors.RESET}")
        return None

def main():
    """Main function"""
    print_header()
    
    # Load configuration
    config = load_config()
    if not config:
        sys.exit(1)
    
    expected_versions = config.get('expected_versions', {})
    
    # Initialize statistics
    stats = {
        'total': 0,
        'correct': 0,
        'wrong': 0,
        'missing': 0
    }
    
    # Count total files
    batch_files = expected_versions.get('batch_files', {})
    python_files = expected_versions.get('python_files', {})
    total_expected = len(batch_files) + len(python_files)
    
    print(f"[INFO] Found configuration for {total_expected} files")
    print()
    
    # Check batch files
    if batch_files:
        check_files_category("BATCH FILES", batch_files, stats)
    
    # Check Python files
    if python_files:
        check_files_category("PYTHON FILES", python_files, stats)
    
    # Print summary
    success = print_summary(stats)

    # Print footer based on final status
    set_last_status(success)
    print_footer(SCRIPT_VERSION)

    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[INFO] Version check interrupted by user{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}[ERROR] Unexpected error: {e}{Colors.RESET}")
        sys.exit(1)

