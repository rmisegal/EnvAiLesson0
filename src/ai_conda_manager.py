#!/usr/bin/env python3
"""
AI Environment Module v3.0.0
Date: 2025-08-12
"""

#!/usr/bin/env python3
"""
AI Environment - Conda Management Module
Handles conda environment activation and verification
"""

import os
import subprocess
from pathlib import Path

try:
    from colorama import Fore, Style
except ImportError:
    class Fore:
        GREEN = RED = YELLOW = CYAN = ""
    class Style:
        RESET_ALL = ""

class CondaManager:
    """Manages conda environment activation for AI Environment"""
    
    def __init__(self, conda_path):
        self.conda_path = Path(conda_path)
        self.conda_exe = self.conda_path / "Scripts" / "conda.exe"
        self.ai_env_path = self.conda_path.parent
        
    def print_info(self, message):
        """Print info message"""
        print(f"{Fore.YELLOW}[INFO] {message}{Style.RESET_ALL}")
        
    def print_success(self, message):
        """Print success message"""
        print(f"{Fore.GREEN}[OK] {message}{Style.RESET_ALL}")
        
    def print_error(self, message):
        """Print error message"""
        print(f"{Fore.RED}[ERROR] {message}{Style.RESET_ALL}")
        
    def setup_conda_paths(self, env_name):
        """Setup conda paths in environment variables"""
        env_path = self.conda_path / "envs" / env_name
        
        # Build new PATH with conda paths first (Windows structure)
        conda_paths = [
            str(env_path),
            str(env_path / "Scripts"),
            str(env_path / "Library" / "bin"),
            str(self.conda_path / "Scripts"),
            str(self.conda_path / "Library" / "bin")
        ]
        
        # Get current PATH and prepend conda paths
        current_path = os.environ.get('PATH', '')
        new_path = ';'.join(conda_paths + [current_path])
        
        # Set environment variables
        os.environ['PATH'] = new_path
        os.environ['CONDA_DEFAULT_ENV'] = env_name
        os.environ['CONDA_PREFIX'] = str(env_path)
        
        self.print_info("Conda paths configured")
        
    def verify_python_location(self):
        """Verify Python is from D: drive"""
        try:
            # First try to get Python executable path directly
            result = subprocess.run(['python', '-c', 'import sys; print(sys.executable)'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=10)
            
            if result.returncode == 0:
                python_path = result.stdout.strip()
                # Normalize path for comparison
                normalized_path = python_path.upper().replace('/', '\\')
                
                # Check multiple possible patterns
                valid_patterns = [
                    "D:\\AI_ENVIRONMENT",
                    "D:/AI_ENVIRONMENT", 
                    "D:\\AI_Environment",
                    "D:/AI_Environment"
                ]
                
                is_valid = any(pattern in normalized_path for pattern in valid_patterns)
                
                if is_valid:
                    self.print_success(f"Using portable Python: {python_path}")
                    return True
                else:
                    self.print_error(f"Python not from D: drive: {python_path}")
                    self.print_info(f"Normalized path: {normalized_path}")
                    self.print_info(f"Looking for patterns: {valid_patterns}")
                    return False
            else:
                # Fallback: try where command if available
                try:
                    result = subprocess.run(['where', 'python'], 
                                          capture_output=True, 
                                          text=True, 
                                          timeout=10)
                    
                    if result.returncode == 0:
                        python_paths = result.stdout.strip().split('\n')
                        first_python = python_paths[0].strip()
                        # Use same normalization logic
                        normalized_path = first_python.upper().replace('/', '\\')
                        
                        valid_patterns = [
                            "D:\\AI_ENVIRONMENT",
                            "D:/AI_ENVIRONMENT", 
                            "D:\\AI_Environment",
                            "D:/AI_Environment"
                        ]
                        
                        is_valid = any(pattern in normalized_path for pattern in valid_patterns)
                        
                        if is_valid:
                            self.print_success(f"Using portable Python: {first_python}")
                            return True
                        else:
                            self.print_error(f"Python not from D: drive: {first_python}")
                            return False
                    else:
                        self.print_error("Could not locate Python executable")
                        return False
                except:
                    self.print_error("Could not verify Python location")
                    return False
                
        except Exception as e:
            self.print_error(f"Failed to verify Python location: {e}")
            return False
            
    def get_python_version(self):
        """Get Python version from activated environment"""
        try:
            result = subprocess.run(['python', '--version'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=10)
            
            if result.returncode == 0:
                version = result.stdout.strip()
                self.print_info(f"Python version: {version}")
                return version
            else:
                self.print_error("Could not get Python version")
                return None
                
        except Exception as e:
            self.print_error(f"Failed to get Python version: {e}")
            return None
            
    def test_conda_environment(self, env_name):
        """Test if conda environment is working"""
        try:
            # Test conda list command
            result = subprocess.run(['conda', 'list'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=15)
            
            if result.returncode == 0:
                self.print_success("Conda environment is functional")
                return True
            else:
                self.print_error("Conda environment test failed")
                return False
                
        except Exception as e:
            self.print_error(f"Conda environment test error: {e}")
            return False
            
    def activate_environment(self, env_name):
        """Activate conda environment"""
        try:
            self.print_info(f"Activating conda environment: {env_name}")
            
            # Setup conda paths
            self.setup_conda_paths(env_name)
            
            # Verify Python location
            if not self.verify_python_location():
                return False
                
            # Get Python version
            self.get_python_version()
            
            # Test conda environment
            if not self.test_conda_environment(env_name):
                return False
                
            self.print_success(f"Conda environment '{env_name}' activated successfully")
            return True
            
        except Exception as e:
            self.print_error(f"Failed to activate conda environment: {e}")
            return False

def main():
    """Test conda manager"""
    conda_path = Path("D:/AI_Environment/Miniconda")
    conda_manager = CondaManager(conda_path)
    
    success = conda_manager.activate_environment("AI2025")
    
    if success:
        print(f"\n{Fore.GREEN}Conda environment activation successful{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}Conda environment activation failed{Style.RESET_ALL}")

if __name__ == "__main__":
    main()

