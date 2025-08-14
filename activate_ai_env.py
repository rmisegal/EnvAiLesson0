#!/usr/bin/env python3
"""
AI Environment Activation Program - Main Entry Point v2.2.0
Portable AI Development Environment with Interactive Menu

Version: 3.0.0
Date: 2025-08-12
Author: AI Environment Team
"""

import sys
import os
from pathlib import Path

# Version information
SCRIPT_VERSION = "3.0.0"
SCRIPT_DATE = "2025-08-11"

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
            
            choice = self.menu_system.get_user_choice(11)
            
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

