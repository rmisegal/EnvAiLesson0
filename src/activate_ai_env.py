#!/usr/bin/env python3
"""
AI Environment Activation Program - Main Entry Point v3.0.18
Portable AI Development Environment with Interactive Menu

Version: 3.0.18 (Dynamic - shows highest system version)
Date: 2025-08-13
Author: AI Environment Team
"""

import sys
import os
import json
from datetime import datetime
from pathlib import Path

def get_highest_version():
    """Get the highest version from version_config.json"""
    try:
        config_path = Path(__file__).parent.parent / "version_config.json"
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Get all versions from the configuration
            versions = []
            
            # Add metadata version
            if 'metadata' in config and 'version' in config['metadata']:
                versions.append(config['metadata']['version'])
            
            # Add all file versions
            if 'expected_versions' in config:
                for category in config['expected_versions'].values():
                    for file_info in category.values():
                        if 'version' in file_info:
                            versions.append(file_info['version'])
            
            # Find the highest version
            if versions:
                # Sort versions by converting to tuples of integers
                def version_key(v):
                    return tuple(map(int, v.split('.')))
                
                highest = max(versions, key=version_key)
                return highest
    except Exception:
        pass
    
    # Fallback to default version
    return "3.0.2"

def get_current_datetime():
    """Get current date and time formatted"""
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M")

# Version information - dynamically determined
SCRIPT_VERSION = get_highest_version()
SCRIPT_DATE = get_current_datetime()

def check_environment():
    """Check if running in proper conda environment"""
    # Check if we're in conda environment
    conda_env = os.environ.get('CONDA_DEFAULT_ENV', '')
    conda_prefix = os.environ.get('CONDA_PREFIX', '')
    
    # Check if psutil is available (indicator of proper environment)
    try:
        import psutil
        psutil_available = True
    except ImportError:
        psutil_available = False
    
    # If not in AI2025 environment or psutil not available, show guidance
    if conda_env != 'AI2025' or not psutil_available:
        print("=" * 70)
        print("⚠️  AI Environment - Incorrect Launch Method")
        print("=" * 70)
        print()
        print("🚫 You are running this script directly outside the conda environment!")
        print()
        print("✅ CORRECT way to launch:")
        print("   D:\\AI_Environment\\run_ai_env.bat")
        print()
        print("❌ INCORRECT (what you did):")
        print("   python activate_ai_env.py")
        print("   python D:\\AI_Environment\\activate_ai_env.py")
        print()
        print("📋 The run_ai_env.bat script will:")
        print("   1. Set up the Python environment")
        print("   2. Activate conda AI2025 environment")
        print("   3. Install required packages (psutil, colorama)")
        print("   4. Launch this script properly")
        print()
        print("🔧 Please use: D:\\AI_Environment\\run_ai_env.bat")
        print("=" * 70)
        
        # Ask user if they want to continue anyway
        try:
            response = input("\nDo you want to continue anyway? (y/N): ").strip().lower()
            if response not in ['y', 'yes']:
                print("\nExiting. Please use run_ai_env.bat for proper setup.")
                sys.exit(1)
            else:
                print("\n⚠️  Continuing with limited functionality...")
                print("   Some features may not work without proper environment setup.\n")
        except KeyboardInterrupt:
            print("\n\nExiting. Please use run_ai_env.bat for proper setup.")
            sys.exit(1)

# Check environment before proceeding
check_environment()

# Add current directory and src directory to Python path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(current_dir / "src"))

try:
    import colorama
    from colorama import Fore, Style
    colorama.init()
except ImportError:
    # Fallback if colorama not available
    class Fore:
        GREEN = RED = YELLOW = CYAN = BLUE = MAGENTA = ""
    class Style:
        RESET_ALL = ""

from ai_menu_system import MenuSystem
from ai_action_handlers import ActionHandlers

class AIEnvironmentActivator:
    """Main AI Environment activation and management system"""
    
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.ai_env_path = Path("D:/AI_Environment")
        self.conda_path = self.ai_env_path / "Miniconda"
        
        # Initialize subsystems
        self.menu_system = MenuSystem(SCRIPT_VERSION, SCRIPT_DATE)
        self.action_handlers = ActionHandlers(self.ai_env_path, self.conda_path)
        
        if self.verbose:
            print(f"{Fore.CYAN}[VERBOSE] {__file__} v{SCRIPT_VERSION} ({SCRIPT_DATE}) starting{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[VERBOSE] AI Environment path: {self.ai_env_path}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[VERBOSE] Conda path: {self.conda_path}{Style.RESET_ALL}")
            
    def print_info(self, message):
        """Print info message"""
        print(f"{Fore.YELLOW}[INFO] {message}{Style.RESET_ALL}")
        
    def run_interactive_menu(self):
        """Run interactive menu system"""
        while True:
            self.menu_system.print_header()
            self.menu_system.print_interactive_menu()
            
            choice = self.menu_system.get_user_choice(15)
            
            if choice == 0:  # Exit
                self.print_info("Exiting AI Environment Manager...")
                break
            elif choice == 1:  # Full activation
                success = self.action_handlers.action_full_activation()
            elif choice == 2:  # Restore PATH
                success = self.action_handlers.action_restore_path()
            elif choice == 3:  # Activate conda only
                success = self.action_handlers.action_activate_conda()
            elif choice == 4:  # Test components
                success = self.action_handlers.action_test_components()
            elif choice == 5:  # Setup Flask
                success = self.action_handlers.action_setup_flask()
            elif choice == 6:  # Setup Ollama
                success = self.action_handlers.action_setup_ollama()
            elif choice == 7:  # Download models
                success = self.action_handlers.action_download_models()
            elif choice == 8:  # Run validation
                success = self.action_handlers.action_run_validation()
            elif choice == 9:  # Launch applications
                self.action_handlers.handle_launch_menu()
                success = True  # Menu operations don't return success/failure
            elif choice == 10:  # Background processes
                self.action_handlers.handle_background_menu()
                success = True  # Menu operations don't return success/failure
            elif choice == 11:  # Advanced options
                self.action_handlers.handle_advanced_menu()
                continue
            elif choice == 12:  # Open AI2025 Terminal
                self.action_handlers.handle_terminal_launcher()
                continue
            elif choice == 13:  # Version & Documentation
                self.action_handlers.handle_help_menu()
                continue
            elif choice == 14:  # Quit (leave processes running)
                self.print_info("Quitting AI Environment Manager...")
                self.print_info("Background processes will continue running")
                break
            elif choice == 15:  # Exit and close all
                self.print_info("Stopping all background processes and exiting...")
                try:
                    from ai_process_manager import BackgroundProcessManager
                    process_manager = BackgroundProcessManager(self.ai_env_path)
                    
                    # Get all tracked processes
                    tracked_processes = process_manager.load_tracked_processes()
                    if tracked_processes:
                        self.print_info(f"Found {len(tracked_processes)} background processes to stop...")
                        
                        # Stop all processes
                        for process_id, process_info in tracked_processes.items():
                            try:
                                pid = process_info.get('pid')
                                name = process_info.get('name', 'Unknown')
                                
                                if pid:
                                    # Try to terminate the process
                                    import subprocess
                                    try:
                                        subprocess.run(['taskkill', '/F', '/PID', str(pid)], 
                                                     check=True, capture_output=True)
                                        self.print_info(f"Stopped {name} (PID: {pid})")
                                    except subprocess.CalledProcessError:
                                        self.print_info(f"Process {name} (PID: {pid}) already stopped")
                            except Exception as e:
                                self.print_info(f"Could not stop process {process_id}: {e}")
                        
                        # Clear the background processes file
                        process_manager.tracked_processes = {}
                        process_manager.save_tracked_processes()
                        self.print_info("All background processes stopped and cleared")
                    else:
                        self.print_info("No background processes found")
                        
                except Exception as e:
                    self.print_info(f"Error stopping background processes: {e}")
                
                self.print_info("Exiting AI Environment Manager...")
                break
            else:
                success = False
                
            # Show result for actions 1-10
            if choice in range(1, 11):
                if success:
                    print(f"\n{Fore.GREEN}✅ Action completed successfully!{Style.RESET_ALL}")
                else:
                    print(f"\n{Fore.RED}❌ Action failed. Check messages above.{Style.RESET_ALL}")
                    
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

def main():
    """Main entry point"""
    # Check for verbose mode
    verbose_mode = "--verbose" in sys.argv
    
    if verbose_mode:
        print(f"{Fore.CYAN}[VERBOSE] Command line arguments: {sys.argv}{Style.RESET_ALL}")
    
    # Create activator instance
    activator = AIEnvironmentActivator(verbose=verbose_mode)
    
    # Check for specific actions
    if len(sys.argv) > 1:
        action = sys.argv[1].lower()
        
        if action == "activate":
            success = activator.action_handlers.action_full_activation()
        elif action == "restore":
            success = activator.action_handlers.action_restore_path()
        elif action == "conda":
            success = activator.action_handlers.action_activate_conda()
        elif action == "status":
            success = activator.action_handlers.action_show_status()
        elif action == "test":
            success = activator.action_handlers.action_test_components()
        elif action == "--verbose":
            # Only --verbose was provided, show status and exit
            if verbose_mode:
                print(f"{Fore.CYAN}[VERBOSE] No action specified, showing status and exiting{Style.RESET_ALL}")
                activator.action_handlers.action_show_status()
            else:
                # Run interactive menu
                activator.run_interactive_menu()
            return
        else:
            print(f"{Fore.RED}[ERROR] Unknown action: {action}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[INFO] Available actions: activate, restore, conda, status, test{Style.RESET_ALL}")
            return
                
        if success:
            print(f"\n{Fore.GREEN}Action completed successfully!{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}Action failed!{Style.RESET_ALL}")
    else:
        # Run interactive menu
        activator.run_interactive_menu()

if __name__ == "__main__":
    main()

