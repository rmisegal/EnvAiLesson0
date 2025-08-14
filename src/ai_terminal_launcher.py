#!/usr/bin/env python3
"""
AI Terminal Launcher
Launches AI2025 terminal with unique prompt and return functionality

Version: 3.0.20
Author: AI Environment Team
Date: 2025-08-13
Time: 12:45
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    class Fore:
        GREEN = YELLOW = CYAN = WHITE = RED = MAGENTA = ""
    class Style:
        RESET_ALL = ""
    COLORAMA_AVAILABLE = False

class TerminalLauncher:
    """Launches AI2025 terminal with enhanced functionality"""
    
    def __init__(self, ai_env_path):
        self.ai_env_path = Path(ai_env_path)
        self.conda_path = self.ai_env_path / "Miniconda"
        self.activate_script = self.conda_path / "Scripts" / "activate.bat"
        
    def create_terminal_script(self):
        """Create enhanced terminal script with return functionality"""
        script_content = f'''@echo off
setlocal EnableDelayedExpansion

:: AI Environment Terminal Launcher v3.0.20
:: Enhanced terminal with return functionality

set "AI_ENV_PATH={self.ai_env_path}"
set "CONDA_PATH={self.conda_path}"

title AI Environment Terminal (AI2025 Active)

echo.
echo {Fore.CYAN}================================================================
echo                   AI Environment Terminal
echo                    AI2025 Environment Active
echo                      Version 3.0.20
echo ================================================================{Style.RESET_ALL}
echo.
echo {Fore.GREEN}✅ AI2025 conda environment is now active{Style.RESET_ALL}
echo {Fore.YELLOW}📁 Working directory: %AI_ENV_PATH%{Style.RESET_ALL}
echo {Fore.CYAN}🐍 Python environment: AI2025{Style.RESET_ALL}
echo.
echo {Fore.WHITE}Available commands:{Style.RESET_ALL}
echo   {Fore.GREEN}python{Style.RESET_ALL}          - Run Python in AI2025 environment
echo   {Fore.GREEN}pip{Style.RESET_ALL}             - Install packages in AI2025 environment
echo   {Fore.GREEN}jupyter lab{Style.RESET_ALL}     - Launch Jupyter Lab
echo   {Fore.GREEN}code .{Style.RESET_ALL}          - Open VS Code in current directory
echo   {Fore.GREEN}return_to_menu{Style.RESET_ALL}  - Return to AI Environment main menu
echo   {Fore.GREEN}exit{Style.RESET_ALL}            - Close this terminal
echo.

:: Activate AI2025 environment
call "%CONDA_PATH%\\Scripts\\activate.bat" AI2025

:: Set custom prompt
set "PROMPT=[AI2025-Terminal] $P$G "

:: Create return_to_menu command
echo @echo off > "%TEMP%\\return_to_menu.bat"
echo echo. >> "%TEMP%\\return_to_menu.bat"
echo echo {Fore.CYAN}🔄 Returning to AI Environment main menu...{Style.RESET_ALL} >> "%TEMP%\\return_to_menu.bat"
echo echo. >> "%TEMP%\\return_to_menu.bat"
echo cd /d "%AI_ENV_PATH%" >> "%TEMP%\\return_to_menu.bat"
echo call run_ai_env.bat >> "%TEMP%\\return_to_menu.bat"

:: Add temp directory to PATH for return_to_menu command
set "PATH=%TEMP%;%PATH%"

:: Change to AI Environment directory
cd /d "%AI_ENV_PATH%"

:: Start interactive command prompt
cmd /k
'''
        
        # Write script to temporary file
        script_path = self.ai_env_path / "temp_terminal_launcher.bat"
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        return script_path
    
    def launch_terminal(self):
        """Launch enhanced AI2025 terminal"""
        try:
            print(f"{Fore.CYAN}🚀 Launching AI2025 Terminal...")
            print(f"{Fore.YELLOW}   - Custom prompt: [AI2025-Terminal]")
            print(f"{Fore.YELLOW}   - Return command: return_to_menu")
            print(f"{Fore.YELLOW}   - Working directory: {self.ai_env_path}")
            
            # Create and execute terminal script
            script_path = self.create_terminal_script()
            
            # Launch terminal
            subprocess.run([str(script_path)], shell=True)
            
            # Clean up temporary script
            if script_path.exists():
                script_path.unlink()
                
            return True
            
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Failed to launch terminal: {e}")
            return False
    
    def create_python_return_function(self):
        """Create Python function for returning to menu from Python scripts"""
        return_function = '''
def return_to_menu():
    """Return to AI Environment main menu from Python"""
    import os
    import subprocess
    
    print("\\n🔄 Returning to AI Environment main menu...")
    ai_env_path = os.environ.get('AI_ENV_PATH', '.')
    subprocess.run([os.path.join(ai_env_path, 'run_ai_env.bat')], shell=True)

# Auto-import return function
print("📋 AI Environment functions loaded:")
print("   - return_to_menu() : Return to main menu")
'''
        
        # Create startup script for Python
        startup_path = self.ai_env_path / "ai_python_startup.py"
        with open(startup_path, 'w', encoding='utf-8') as f:
            f.write(return_function)
        
        return startup_path

def main():
    """Main function for standalone execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Terminal Launcher')
    parser.add_argument('--ai-env-path', default='.', 
                       help='Path to AI Environment directory')
    
    args = parser.parse_args()
    
    launcher = TerminalLauncher(args.ai_env_path)
    success = launcher.launch_terminal()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

