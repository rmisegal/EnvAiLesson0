#!/usr/bin/env python3
"""
AI Environment Module v3.0.17
Date: 2025-08-13
Time: 05:30
"""

#!/usr/bin/env python3
"""
AI Environment - Application Launcher Module
Handles launching various applications in background mode with enhanced VS Code integration
"""

import subprocess
import webbrowser
import time
from pathlib import Path

try:
    from colorama import Fore, Style
except ImportError:
    class Fore:
        GREEN = RED = YELLOW = CYAN = BLUE = MAGENTA = ""
    class Style:
        RESET_ALL = ""

from ai_process_manager import BackgroundProcessManager

class ApplicationLauncher:
    """Launches and manages various AI development applications"""
    
    def __init__(self, ai_env_path):
        self.ai_env_path = Path(ai_env_path)
        self.process_manager = BackgroundProcessManager(ai_env_path)
        
    def print_info(self, message):
        """Print info message"""
        print(f"{Fore.YELLOW}[INFO] {message}{Style.RESET_ALL}")
        
    def print_success(self, message):
        """Print success message"""
        print(f"{Fore.GREEN}[OK] {message}{Style.RESET_ALL}")
        
    def print_error(self, message):
        """Print error message"""
        print(f"{Fore.RED}[ERROR] {message}{Style.RESET_ALL}")
        
    def print_warning(self, message):
        """Print warning message"""
        print(f"{Fore.YELLOW}[WARNING] {message}{Style.RESET_ALL}")
        
    def launch_vscode(self, project_path=None):
        """Launch VS Code with project"""
        print(f"\n{Fore.BLUE}🔧 Launching VS Code...{Style.RESET_ALL}")
        
        if project_path is None:
            # Show project selection menu
            projects_dir = self.ai_env_path / "Projects"
            projects_dir.mkdir(exist_ok=True)
            
            print(f"\n{Fore.CYAN}📁 Available Projects:{Style.RESET_ALL}")
            print(f"{Fore.YELLOW} 1.{Style.RESET_ALL} Open Projects folder")
            print(f"{Fore.YELLOW} 2.{Style.RESET_ALL} Open AI Environment root")
            print(f"{Fore.YELLOW} 3.{Style.RESET_ALL} Open current directory")
            print(f"{Fore.YELLOW} 0.{Style.RESET_ALL} Cancel")
            
            try:
                choice = int(input(f"\n{Fore.CYAN}Select project to open (0-3): {Style.RESET_ALL}"))
                
                if choice == 0:
                    return False
                elif choice == 1:
                    project_path = projects_dir
                elif choice == 2:
                    project_path = self.ai_env_path
                elif choice == 3:
                    project_path = Path.cwd()
                else:
                    self.print_error("Invalid choice")
                    return False
                    
            except ValueError:
                self.print_error("Invalid input")
                return False
                
        success = self.process_manager.launch_vscode(project_path)
        if success:
            self.print_info("VS Code is now running in background")
            self.print_info("Use 'Background Processes' menu to manage it")
        return success
        
    def launch_jupyter(self):
        """Launch Jupyter Lab"""
        print(f"\n{Fore.BLUE}📊 Launching Jupyter Lab...{Style.RESET_ALL}")
        
        success = self.process_manager.launch_jupyter()
        if success:
            self.print_info("Jupyter Lab is now running in background")
            self.print_info("Use 'Background Processes' menu to manage it")
            
            # Ask if user wants to open browser
            try:
                open_browser = input(f"\n{Fore.CYAN}Open Jupyter Lab in browser? (y/n): {Style.RESET_ALL}").lower()
                if open_browser in ['y', 'yes']:
                    time.sleep(3)  # Wait for server to start
                    webbrowser.open('http://localhost:8888')
                    self.print_success("Jupyter Lab opened in browser")
            except:
                pass
                
        return success
        
    def launch_streamlit_demo(self):
        """Launch Streamlit demo application"""
        print(f"\n{Fore.BLUE}🌟 Launching Streamlit Demo...{Style.RESET_ALL}")
        
        success = self.process_manager.launch_streamlit_demo()
        if success:
            self.print_info("Streamlit demo is now running in background")
            self.print_info("Use 'Background Processes' menu to manage it")
            
            # Ask if user wants to open browser
            try:
                open_browser = input(f"\n{Fore.CYAN}Open Streamlit demo in browser? (y/n): {Style.RESET_ALL}").lower()
                if open_browser in ['y', 'yes']:
                    time.sleep(3)  # Wait for server to start
                    webbrowser.open('http://localhost:8501')
                    self.print_success("Streamlit demo opened in browser")
            except:
                pass
                
        return success
        
    def launch_python_repl(self):
        """Launch Python REPL in new terminal"""
        print(f"\n{Fore.BLUE}🐍 Launching Python REPL...{Style.RESET_ALL}")
        
        try:
            # Launch Python in a new command prompt window
            cmd = f'start "Python REPL - AI Environment" cmd /k "python"'
            
            success = self.process_manager.launch_custom_command(
                cmd, 
                "Python REPL",
                self.ai_env_path
            )
            
            if success:
                self.print_success("Python REPL launched in new terminal window")
                self.print_info("Use 'Background Processes' menu to manage it")
            return success
            
        except Exception as e:
            self.print_error(f"Failed to launch Python REPL: {e}")
            return False
            
    def launch_conda_prompt(self):
        """Launch Conda prompt in new terminal"""
        print(f"\n{Fore.BLUE}🔧 Launching Conda Prompt...{Style.RESET_ALL}")
        
        try:
            # Activate conda environment and open prompt
            conda_exe = self.ai_env_path / "Miniconda" / "Scripts" / "conda.exe"
            cmd = f'start "Conda Prompt - AI2025" cmd /k "{conda_exe} activate AI2025"'
            
            success = self.process_manager.launch_custom_command(
                cmd,
                "Conda Prompt", 
                self.ai_env_path
            )
            
            if success:
                self.print_success("Conda prompt launched in new terminal window")
                self.print_info("Use 'Background Processes' menu to manage it")
            return success
            
        except Exception as e:
            self.print_error(f"Failed to launch Conda prompt: {e}")
            return False
            
    def launch_file_explorer(self):
        """Launch File Explorer in AI Environment directory"""
        print(f"\n{Fore.BLUE}📁 Opening File Explorer...{Style.RESET_ALL}")
        
        try:
            cmd = f'explorer "{self.ai_env_path}"'
            
            success = self.process_manager.launch_custom_command(
                cmd,
                "File Explorer",
                self.ai_env_path
            )
            
            if success:
                self.print_success("File Explorer opened")
                self.print_info("Use 'Background Processes' menu to manage it")
            return success
            
        except Exception as e:
            self.print_error(f"Failed to open File Explorer: {e}")
            return False
            
    def launch_tensorboard(self, log_dir=None):
        """Launch TensorBoard"""
        print(f"\n{Fore.BLUE}📈 Launching TensorBoard...{Style.RESET_ALL}")
        
        if log_dir is None:
            log_dir = self.ai_env_path / "Projects" / "logs"
            log_dir.mkdir(parents=True, exist_ok=True)
            
        try:
            cmd = f'tensorboard --logdir="{log_dir}" --port=6006'
            
            success = self.process_manager.launch_custom_command(
                cmd,
                "TensorBoard",
                self.ai_env_path
            )
            
            if success:
                self.print_success("TensorBoard launched successfully")
                self.print_info("Access TensorBoard at: http://localhost:6006")
                self.print_info("Use 'Background Processes' menu to manage it")
                
                # Ask if user wants to open browser
                try:
                    open_browser = input(f"\n{Fore.CYAN}Open TensorBoard in browser? (y/n): {Style.RESET_ALL}").lower()
                    if open_browser in ['y', 'yes']:
                        time.sleep(3)  # Wait for server to start
                        webbrowser.open('http://localhost:6006')
                        self.print_success("TensorBoard opened in browser")
                except:
                    pass
                    
            return success
            
        except Exception as e:
            self.print_error(f"Failed to launch TensorBoard: {e}")
            return False
            
    def launch_mlflow_ui(self):
        """Launch MLflow UI"""
        print(f"\n{Fore.BLUE}🔬 Launching MLflow UI...{Style.RESET_ALL}")
        
        try:
            # Set MLflow tracking directory
            mlflow_dir = self.ai_env_path / "Projects" / "mlruns"
            mlflow_dir.mkdir(parents=True, exist_ok=True)
            
            cmd = f'mlflow ui --backend-store-uri "file:///{mlflow_dir}" --port=5000'
            
            success = self.process_manager.launch_custom_command(
                cmd,
                "MLflow UI",
                self.ai_env_path
            )
            
            if success:
                self.print_success("MLflow UI launched successfully")
                self.print_info("Access MLflow UI at: http://localhost:5000")
                self.print_info("Use 'Background Processes' menu to manage it")
                
                # Ask if user wants to open browser
                try:
                    open_browser = input(f"\n{Fore.CYAN}Open MLflow UI in browser? (y/n): {Style.RESET_ALL}").lower()
                    if open_browser in ['y', 'yes']:
                        time.sleep(3)  # Wait for server to start
                        webbrowser.open('http://localhost:5000')
                        self.print_success("MLflow UI opened in browser")
                except:
                    pass
                    
            return success
            
        except Exception as e:
            self.print_error(f"Failed to launch MLflow UI: {e}")
            return False
            
    def show_launch_menu(self):
        """Show application launch menu"""
        print(f"\n{Fore.MAGENTA}🚀 Application Launcher:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW} 1.{Style.RESET_ALL} 🔧 VS Code")
        print(f"{Fore.YELLOW} 2.{Style.RESET_ALL} 📊 Jupyter Lab")
        print(f"{Fore.YELLOW} 3.{Style.RESET_ALL} 🌟 Streamlit Demo")
        print(f"{Fore.YELLOW} 4.{Style.RESET_ALL} 🐍 Python REPL")
        print(f"{Fore.YELLOW} 5.{Style.RESET_ALL} 🔧 Conda Prompt")
        print(f"{Fore.YELLOW} 6.{Style.RESET_ALL} 📁 File Explorer")
        print(f"{Fore.YELLOW} 7.{Style.RESET_ALL} 📈 TensorBoard")
        print(f"{Fore.YELLOW} 8.{Style.RESET_ALL} 🔬 MLflow UI")
        print(f"{Fore.YELLOW} 0.{Style.RESET_ALL} ⬅️  Back")
        print()
        
    def handle_launch_choice(self, choice):
        """Handle application launch choice"""
        if choice == 1:
            return self.launch_vscode()
        elif choice == 2:
            return self.launch_jupyter()
        elif choice == 3:
            return self.launch_streamlit_demo()
        elif choice == 4:
            return self.launch_python_repl()
        elif choice == 5:
            return self.launch_conda_prompt()
        elif choice == 6:
            return self.launch_file_explorer()
        elif choice == 7:
            return self.launch_tensorboard()
        elif choice == 8:
            return self.launch_mlflow_ui()
        else:
            return False

def main():
    """Test application launcher"""
    ai_env_path = Path("D:/AI_Environment")
    app_launcher = ApplicationLauncher(ai_env_path)
    
    print("Testing Application Launcher...")
    app_launcher.show_launch_menu()

if __name__ == "__main__":
    main()

