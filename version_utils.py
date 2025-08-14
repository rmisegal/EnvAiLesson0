import os

class Colors:
    """Cross-platform color codes"""
    if os.name == 'nt':  # Windows
        RESET = ''
        CYAN = ''
        GREEN = ''
        YELLOW = ''
        RED = ''
        BLUE = ''
        MAGENTA = ''
    else:  # Unix/Linux/Mac
        RESET = '[0m'
        CYAN = '[96m'
        GREEN = '[92m'
        YELLOW = '[93m'
        RED = '[91m'
        BLUE = '[94m'
        MAGENTA = '[95m'


def check_file_version(filepath, expected_version, search_pattern, description=""):
    """Check if a file contains the expected version"""
    try:
        if not os.path.exists(filepath):
            return False, "FILE NOT FOUND", "missing"

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        if search_pattern:
            if search_pattern in content:
                return True, f"Version {expected_version} found", "correct"
            else:
                return False, f"Version {expected_version} NOT found", "wrong"
        else:
            file_ext = os.path.splitext(filepath)[1].lower()

            if file_ext == '.bat':
                patterns = [
                    f'SCRIPT_VERSION={expected_version}',
                    f'SCRIPT_VERSION="{expected_version}"',
                    f'v{expected_version}'
                ]
            elif file_ext == '.py':
                patterns = [
                    f'SCRIPT_VERSION = "{expected_version}"',
                    f'AI Environment Module v{expected_version}',
                    f'Version: {expected_version}',
                    f'Version {expected_version}'
                ]
            else:
                patterns = [
                    f'v{expected_version}',
                    f'Version {expected_version}',
                    expected_version,
                ]

            for pattern in patterns:
                if pattern in content:
                    return True, f"Version {expected_version} found", "correct"

            return False, f"Version {expected_version} NOT found", "wrong"

    except Exception as e:
        return False, f"ERROR: {e}", "error"


def check_files_category(category_name, files_dict, stats):
    """Check a category of files (batch or python)"""
    print("================================================================")
    print(f"                       {category_name.upper()}")
    print("================================================================")
    print(f"[*] Checking {category_name.lower()} files from JSON configuration...")
    print()

    for filename, info in files_dict.items():
        stats['total'] += 1
        expected_version = info['version']
        search_pattern = info.get('search_pattern', '')
        description = info.get('description', '')

        print(f"[*] Checking: {filename} (expected: {expected_version})")

        success, message, status = check_file_version(filename, expected_version, search_pattern, description)

        if success:
            print(f"{Colors.GREEN}[OK] {filename} - {message}{Colors.RESET}")
            stats['correct'] += 1
        else:
            if status == "missing":
                print(f"{Colors.RED}[ERROR] {filename} - {message}{Colors.RESET}")
                stats['missing'] += 1
            else:
                print(f"{Colors.YELLOW}[WARNING] {filename} - {message}{Colors.RESET}")
                stats['wrong'] += 1
        print()


def print_summary(stats):
    """Print the summary statistics"""
    print("================================================================")
    print("                       VERSION SUMMARY")
    print("================================================================")
    print()
    print(f"Total files checked: {stats['total']}")
    print(f"Files with correct version: {stats['correct']}")
    print(f"Files with wrong version: {stats['wrong']}")
    print(f"Files missing: {stats['missing']}")
    print()

    if stats['correct'] == stats['total'] and stats['total'] > 0:
        percentage = 100.0
        print(f"{Colors.GREEN}[SUCCESS] All files have correct versions ({percentage:.0f}%){Colors.RESET}")
        print(f"{Colors.GREEN}[INFO] Your AI Environment system is up to date!{Colors.RESET}")
        return True
    else:
        percentage = (stats['correct'] / stats['total']) * 100 if stats['total'] > 0 else 0
        print(f"{Colors.YELLOW}[WARNING] Only {stats['correct']}/{stats['total']} files have correct versions ({percentage:.0f}%){Colors.RESET}")
        print()

        if stats['wrong'] > 0:
            print(f"{Colors.YELLOW}[ACTION REQUIRED] {stats['wrong']} files have wrong versions{Colors.RESET}")
        if stats['missing'] > 0:
            print(f"{Colors.RED}[ACTION REQUIRED] {stats['missing']} files are missing{Colors.RESET}")

        print(f"{Colors.CYAN}[SOLUTION] Check version_config.json for expected versions{Colors.RESET}")
        print(f"{Colors.CYAN}[SOLUTION] Update files as needed or download latest package{Colors.RESET}")
        return False


def print_footer(success):
    """Print the footer information"""
    print()
    print("================================================================")
    print("                   JSON CONFIGURATION INFO")
    print("================================================================")
    print()
    print(f"[INFO] Configuration file: version_config.json")
    print(f"[INFO] Script version: 3.0.0")
    print(f"[INFO] To view detailed version requirements:")
    if os.name == 'nt':  # Windows
        print("  type version_config.json")
    else:  # Unix/Linux/Mac
        print("  cat version_config.json")
    print()
    print(f"[INFO] To update expected versions:")
    print("  Edit version_config.json with your preferred text editor")
    print()
    print("================================================================")
    print("                   VERSION CHECK COMPLETE")
    print("================================================================")
