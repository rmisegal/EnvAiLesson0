#!/usr/bin/env python3
"""
AI Environment Module v3.0.18
Date: 2025-08-13
"""

#!/usr/bin/env python3
"""
AI Environment - Component Setup Module
Handles Flask, Ollama, and other component setup
"""

import subprocess
from pathlib import Path

try:
    from colorama import Fore, Style
except ImportError:
    class Fore:
        GREEN = RED = YELLOW = CYAN = ""
    class Style:
        RESET_ALL = ""

class ComponentSetup:
    """Manages component setup for AI Environment"""
    
    def __init__(self, ai_env_path):
        self.ai_env_path = Path(ai_env_path)
        self.ollama_exe = self.ai_env_path / "Ollama" / "ollama.exe"
        
    def print_info(self, message):
        """Print info message"""
        print(f"{Fore.YELLOW}[INFO] {message}{Style.RESET_ALL}")
        
    def print_success(self, message):
        """Print success message"""
        print(f"{Fore.GREEN}[OK] {message}{Style.RESET_ALL}")
        
    def print_error(self, message):
        """Print error message"""
        print(f"{Fore.RED}[ERROR] {message}{Style.RESET_ALL}")
        
    def setup_flask(self):
        """Setup Flask package"""
        try:
            # Check if Flask is already installed
            result = subprocess.run(['python', '-c', 'import flask; print(flask.__version__)'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=10)
            
            if result.returncode == 0:
                version = result.stdout.strip()
                self.print_success(f"Flask already installed (version {version})")
                return True
            else:
                self.print_info("Flask not found. Installing...")
                result = subprocess.run(['pip', 'install', 'flask'], 
                                      capture_output=True, 
                                      text=True, 
                                      timeout=60)
                
                if result.returncode == 0:
                    self.print_success("Flask installed successfully")
                    return True
                else:
                    self.print_error(f"Failed to install Flask: {result.stderr}")
                    return False
                    
        except Exception as e:
            self.print_error(f"Flask setup error: {e}")
            return False
            
    def setup_ollama(self):
        """Setup Ollama server"""
        try:
            if not self.ollama_exe.exists():
                self.print_error(f"Ollama not found at {self.ollama_exe}")
                return False
                
            # Check if Ollama is already running
            result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq ollama.exe'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=10)
            
            if 'ollama.exe' in result.stdout:
                self.print_success("Ollama server is already running")
                return True
            else:
                self.print_info("Starting Ollama server...")
                process = subprocess.Popen([str(self.ollama_exe), 'serve'], 
                               creationflags=subprocess.CREATE_NEW_CONSOLE)
                
                # Track the process
                try:
                    from ai_process_manager import BackgroundProcessManager
                    process_manager = BackgroundProcessManager(self.ai_env_path)
                    process_manager.track_process(
                        process_id="ollama_server_component_setup",
                        name="Ollama Server (Component Setup)",
                        pid=process.pid,
                        command=f"{self.ollama_exe} serve",
                        url="http://127.0.0.1:11434"
                    )
                except Exception as e:
                    self.print_warning(f"Could not track Ollama process: {e}")
                
                # Wait and verify
                import time
                time.sleep(3)
                
                result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq ollama.exe'], 
                                      capture_output=True, 
                                      text=True, 
                                      timeout=10)
                
                if 'ollama.exe' in result.stdout:
                    self.print_success("Ollama server started successfully")
                    return True
                else:
                    self.print_error("Failed to start Ollama server")
                    return False
                    
        except Exception as e:
            self.print_error(f"Ollama setup error: {e}")
            return False
            
    def setup_all_components(self):
        """Setup all components"""
        try:
            self.print_info("Setting up Flask...")
            if not self.setup_flask():
                return False
                
            self.print_info("Setting up Ollama...")
            if not self.setup_ollama():
                return False
                
            return True
            
        except Exception as e:
            self.print_error(f"Component setup error: {e}")
            return False

def main():
    """Test component setup"""
    ai_env_path = Path("D:/AI_Environment")
    component_setup = ComponentSetup(ai_env_path)
    
    success = component_setup.setup_all_components()
    
    if success:
        print(f"\n{Fore.GREEN}Component setup completed successfully{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}Component setup failed{Style.RESET_ALL}")

if __name__ == "__main__":
    main()

