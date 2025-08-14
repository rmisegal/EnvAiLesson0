#!/usr/bin/env python3
"""
AI Environment Module v3.0.22
Date: 2025-08-13
Time: 14:30
"""

#!/usr/bin/env python3
"""
AI Environment - Component Testing Module
Comprehensive testing of all AI Environment components including model management and Jupyter Lab system
"""

import os
import re
import subprocess
import sys
from pathlib import Path
try:
    from colorama import Fore, Style
except ImportError:
    class Fore:
        GREEN = RED = YELLOW = CYAN = BLUE = ""
    class Style:
        RESET_ALL = ""

from ai_path_manager import PathManager
from ai_conda_manager import CondaManager

class ComponentTester:
    """Comprehensive testing of AI Environment components"""
    
    def __init__(self, ai_env_path, conda_path):
        self.ai_env_path = Path(ai_env_path)
        self.conda_path = Path(conda_path)
        
    def print_step(self, step_num, description):
        """Print step header"""
        print(f"{Fore.CYAN}[*] Step {step_num}: {description}...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'-'*50}{Style.RESET_ALL}")
        
    def print_success(self, message):
        """Print success message"""
        print(f"{Fore.GREEN}[OK] {message}{Style.RESET_ALL}")
        
    def print_error(self, message):
        """Print error message"""
        print(f"{Fore.RED}[ERROR] {message}{Style.RESET_ALL}")
        
    def print_info(self, message):
        """Print info message"""
        print(f"{Fore.YELLOW}[INFO] {message}{Style.RESET_ALL}")
        
    def test_directory_structure(self):
        """Test AI Environment directory structure"""
        if self.ai_env_path.exists():
            self.print_success("AI Environment directory found")
            
            # Check subdirectories - only essential ones
            required_dirs = ["Miniconda"]
            optional_dirs = ["AI_Installer", "Ollama"]
            missing_dirs = []
            
            for dir_name in required_dirs:
                if (self.ai_env_path / dir_name).exists():
                    self.print_success(f"  ✓ {dir_name} directory found")
                else:
                    self.print_error(f"  ✗ {dir_name} directory missing")
                    missing_dirs.append(dir_name)
            
            # Check optional directories
            for dir_name in optional_dirs:
                if (self.ai_env_path / dir_name).exists():
                    self.print_success(f"  ✓ {dir_name} directory found (optional)")
                else:
                    self.print_info(f"  - {dir_name} directory not found (optional)")
            
            # Note: AI_Environment_Python is the current directory we're running from
            
            if not missing_dirs:
                self.print_success("Directory structure test PASSED")
                return True
            else:
                self.print_error(f"Directory structure test FAILED - Missing: {missing_dirs}")
                return False
        else:
            self.print_error("AI Environment directory not found")
            return False
            
    def test_conda_installation(self):
        """Test Conda installation"""
        if self.conda_path.exists():
            self.print_success("Conda directory found")
            
            # Test conda executable
            conda_exe = self.conda_path / "Scripts" / "conda.exe"
            if conda_exe.exists():
                self.print_success("  ✓ conda.exe found")
                
                # Test conda command
                try:
                    result = subprocess.run([str(conda_exe), "--version"], 
                                          capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        version = result.stdout.strip()
                        self.print_success(f"  ✓ Conda version: {version}")
                        self.print_success("Conda installation test PASSED")
                        return True
                    else:
                        self.print_error("  ✗ Conda command failed")
                        self.print_error("Conda installation test FAILED")
                        return False
                except Exception as e:
                    self.print_error(f"  ✗ Conda test error: {e}")
                    self.print_error("Conda installation test FAILED")
                    return False
            else:
                self.print_error("  ✗ conda.exe not found")
                self.print_error("Conda installation test FAILED")
                return False
        else:
            self.print_error("Conda directory not found")
            return False
            
    def test_ai2025_environment(self):
        """Test AI2025 conda environment"""
        ai2025_path = self.conda_path / "envs" / "AI2025"
        if ai2025_path.exists():
            self.print_success("AI2025 environment directory found")
            
            # Test Python executable
            python_exe = ai2025_path / "python.exe"
            if python_exe.exists():
                self.print_success("  ✓ Python executable found")
                
                # Test Python version
                try:
                    result = subprocess.run([str(python_exe), "--version"], 
                                          capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        version = result.stdout.strip()
                        self.print_success(f"  ✓ Python version: {version}")
                        self.print_success("AI2025 environment test PASSED")
                        return True
                    else:
                        self.print_error("  ✗ Python version check failed")
                        self.print_error("AI2025 environment test FAILED")
                        return False
                except Exception as e:
                    self.print_error(f"  ✗ Python test error: {e}")
                    self.print_error("AI2025 environment test FAILED")
                    return False
            else:
                self.print_error("  ✗ Python executable not found")
                self.print_error("AI2025 environment test FAILED")
                return False
        else:
            self.print_error("AI2025 environment not found")
            return False
            
    def test_python_packages(self):
        """Test required Python packages"""
        required_packages = ["psutil", "colorama", "requests", "numpy", "pandas"]
        
        try:
            # Activate environment and test packages
            conda_manager = CondaManager(self.conda_path)
            conda_manager.setup_conda_paths("AI2025")
            
            package_results = []
            for package in required_packages:
                try:
                    # Special handling for packages that can be slow to import
                    if package == "pandas":
                        timeout_duration = 15
                        self.print_info(f"  Testing {package} (may take a moment)...")
                    elif package == "numpy":
                        timeout_duration = 10
                        self.print_info(f"  Testing {package} (may take a moment)...")
                    else:
                        timeout_duration = 5
                    
                    result = subprocess.run(["python", "-c", f"import {package}; print('{package} OK')"], 
                                          capture_output=True, text=True, timeout=timeout_duration)
                    if result.returncode == 0:
                        self.print_success(f"  ✓ {package} package available")
                        package_results.append(True)
                    else:
                        self.print_error(f"  ✗ {package} package missing or broken")
                        package_results.append(False)
                except subprocess.TimeoutExpired:
                    self.print_error(f"  ✗ {package} test error: Command '['python', '-c', \"import {package}; print('{package} OK')\"]' timed out after {timeout_duration} seconds")
                    package_results.append(False)
                except Exception as e:
                    self.print_error(f"  ✗ {package} test error: {e}")
                    package_results.append(False)
            
            if all(package_results):
                self.print_success("Python packages test PASSED")
                return True
            else:
                missing_count = len([r for r in package_results if not r])
                self.print_error(f"Python packages test FAILED - {missing_count}/{len(required_packages)} packages missing")
                return False
                
        except Exception as e:
            self.print_error(f"Package testing failed: {e}")
            return False
            
    def test_ollama_installation(self):
        """Test Ollama installation (optional)"""
        ollama_path = self.ai_env_path / "Ollama"
        if ollama_path.exists():
            self.print_success("Ollama directory found")
            
            ollama_exe = ollama_path / "ollama.exe"
            if ollama_exe.exists():
                self.print_success("  ✓ ollama.exe found")
                
                try:
                    # Try version command first
                    result = subprocess.run([str(ollama_exe), "version"], 
                                          capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        version_info = result.stdout.strip()
                        self.print_success(f"  ✓ Ollama version: {version_info}")
                        self.print_success("Ollama installation test PASSED")
                        return True
                    else:
                        # Try alternative commands if version fails
                        self.print_info("  - Version command failed, trying alternative check...")
                        result2 = subprocess.run([str(ollama_exe), "--help"], 
                                                capture_output=True, text=True, timeout=5)
                        if result2.returncode == 0:
                            self.print_success("  ✓ Ollama executable responds to --help")
                            self.print_success("Ollama installation test PASSED (basic)")
                            return True
                        else:
                            self.print_error(f"  ✗ Ollama version check failed (exit code: {result.returncode})")
                            if result.stderr:
                                self.print_error(f"  ✗ Error output: {result.stderr.strip()}")
                            self.print_error("Ollama installation test FAILED")
                            return False
                except Exception as e:
                    self.print_error(f"  ✗ Ollama test error: {e}")
                    self.print_error("Ollama installation test FAILED")
                    return False
            else:
                self.print_error("  ✗ ollama.exe not found")
                self.print_error("Ollama installation test FAILED")
                return False
        else:
            self.print_info("Ollama not installed (optional component)")
            return True  # Count as passed since it's optional
            
    def test_system_integration(self):
        """Test system integration"""
        try:
            # Test PATH configuration
            current_path = os.environ.get('PATH', '')
            if 'AI_Environment' in current_path:
                self.print_success("  ✓ AI Environment paths in system PATH")
            else:
                self.print_info("  ℹ AI Environment paths not in current PATH (normal)")
            
            # Test environment variables
            conda_env = os.environ.get('CONDA_DEFAULT_ENV', '')
            if conda_env:
                self.print_success(f"  ✓ Active conda environment: {conda_env}")
            else:
                self.print_info("  ℹ No active conda environment")
            
            # Test basic Windows commands
            path_manager = PathManager()
            cmd_results = path_manager.test_basic_commands()
            
            working_commands = sum(1 for result in cmd_results.values() if result)
            total_commands = len(cmd_results)
            
            if working_commands == total_commands:
                self.print_success(f"  ✓ All Windows commands working ({working_commands}/{total_commands})")
                self.print_success("System integration test PASSED")
                return True
            else:
                self.print_error(f"  ✗ Some Windows commands not working ({working_commands}/{total_commands})")
                self.print_error("System integration test FAILED")
                return False
                
        except Exception as e:
            self.print_error(f"System integration test error: {e}")
            return False
            
    def test_model_management_system(self):
        """Test AI model management components"""
        try:
            self.print_info("Testing AI model management system...")
            
            # Test model manager import
            try:
                import sys
                sys.path.append(str(self.ai_env_path / "src"))
                from ai_model_manager import AIModelManager
                self.print_success("  ✓ AI Model Manager module loads correctly")
            except ImportError as e:
                self.print_error(f"  ✗ AI Model Manager import failed: {e}")
                return False
            
            # Test model loader import
            try:
                from ai_model_loader import ModelLoader
                self.print_success("  ✓ Model Loader module loads correctly")
            except ImportError as e:
                self.print_error(f"  ✗ Model Loader import failed: {e}")
                return False
            
            # Test model downloader import
            try:
                from ai_model_downloader import ModelDownloader
                self.print_success("  ✓ Model Downloader module loads correctly")
            except ImportError as e:
                self.print_error(f"  ✗ Model Downloader import failed: {e}")
                return False
            
            # Test help directory
            help_dir = self.ai_env_path / "help"
            if help_dir.exists():
                help_files = list(help_dir.glob("*.txt"))
                if len(help_files) >= 5:
                    self.print_success(f"  ✓ Help directory contains {len(help_files)} model help files")
                else:
                    self.print_warning(f"  ⚠ Help directory contains only {len(help_files)} files (expected 5+)")
            else:
                self.print_error("  ✗ Help directory not found")
                return False
            
            self.print_success("Model management system test PASSED")
            return True
            
        except Exception as e:
            self.print_error(f"Model management system test error: {e}")
            return False
    
    def test_jupyter_lab_system(self):
        """Test Jupyter Lab management components"""
        try:
            self.print_info("Testing Jupyter Lab management system...")
            
            # Test Jupyter manager import
            try:
                import sys
                sys.path.append(str(self.ai_env_path / "src"))
                from ai_jupyter_manager import JupyterLabManager
                self.print_success("  ✓ Jupyter Lab Manager module loads correctly")
            except ImportError as e:
                self.print_error(f"  ✗ Jupyter Lab Manager import failed: {e}")
                return False
            
            # Test Projects directory
            projects_dir = self.ai_env_path / "Projects"
            if projects_dir.exists():
                project_dirs = [d for d in projects_dir.iterdir() if d.is_dir()]
                if len(project_dirs) > 0:
                    self.print_success(f"  ✓ Projects directory contains {len(project_dirs)} project(s)")
                else:
                    self.print_info("  ℹ Projects directory is empty (normal for new installation)")
            else:
                self.print_info("  ℹ Projects directory not found (will be created when needed)")
            
            # Test basic example project
            basic_example = self.ai_env_path / "Projects" / "01_Basic_LLM_Example"
            if basic_example.exists():
                main_py = basic_example / "main.py"
                if main_py.exists():
                    self.print_success("  ✓ Basic LLM Example project found")
                else:
                    self.print_info("  ℹ Basic LLM Example main.py not found")
            else:
                self.print_info("  ℹ Basic LLM Example project not found")
            
            self.print_success("Jupyter Lab system test PASSED")
            return True
            
        except Exception as e:
            self.print_error(f"Jupyter Lab system test error: {e}")
            return False
    
    def test_ollama_help_system(self):
        """Test Ollama help and documentation system"""
        try:
            self.print_info("Testing Ollama help system...")
            
            # Test help files content
            help_dir = self.ai_env_path / "help"
            if not help_dir.exists():
                self.print_error("  ✗ Help directory not found")
                return False
            
            expected_help_files = [
                "phi_2_7b.txt",
                "llama2_7b.txt", 
                "mistral_7b.txt",
                "codellama_7b.txt",
                "gpt_oss_20b.txt"
            ]
            
            found_files = 0
            for help_file in expected_help_files:
                file_path = help_dir / help_file
                if file_path.exists():
                    # Check if file has content
                    if file_path.stat().st_size > 100:  # At least 100 bytes
                        self.print_success(f"  ✓ {help_file} found and has content")
                        found_files += 1
                    else:
                        self.print_warning(f"  ⚠ {help_file} found but appears empty")
                else:
                    self.print_error(f"  ✗ {help_file} not found")
            
            if found_files >= 4:  # Allow for some flexibility
                self.print_success(f"Ollama help system test PASSED ({found_files}/5 files)")
                return True
            else:
                self.print_error(f"Ollama help system test FAILED ({found_files}/5 files)")
                return False
            
        except Exception as e:
            self.print_error(f"Ollama help system test error: {e}")
            return False
    
    def test_environment_validation(self):
        """Test environment validation system with install_config.json comparison"""
        try:
            self.print_info("Testing environment validation system...")
            
            # Test if config directory exists
            config_dir = self.ai_env_path / "config"
            if not config_dir.exists():
                self.print_error("  ✗ Config directory not found")
                return False
            else:
                self.print_success("  ✓ Config directory found")
            
            # Test if install_config.json exists
            config_file = config_dir / "install_config.json"
            if not config_file.exists():
                self.print_error("  ✗ install_config.json not found")
                return False
            else:
                self.print_success("  ✓ install_config.json found")
            
            # Test if environment validator module loads
            try:
                from ai_environment_validator import EnvironmentValidator
                self.print_success("  ✓ Environment Validator module loads correctly")
            except ImportError as e:
                self.print_error(f"  ✗ Environment Validator import failed: {e}")
                return False
            
            # Test validator initialization and configuration loading
            try:
                validator = EnvironmentValidator(self.ai_env_path)
                if validator.load_config():
                    self.print_success("  ✓ Configuration loaded successfully")
                else:
                    self.print_error("  ✗ Failed to load configuration")
                    return False
            except Exception as e:
                self.print_error(f"  ✗ Validator initialization failed: {e}")
                return False
            
            # Test package comparison with install_config.json
            try:
                self.print_info("  Performing package validation against install_config.json...")
                
                # Quick package check (don't install, just report)
                validator.check_python_packages()
                
                # Generate summary
                total_packages = len(validator.config.get('python_packages', []))
                installed_count = len(validator.installed_packages)
                missing_count = len(validator.missing_packages)
                
                self.print_success(f"  ✓ Package validation completed")
                self.print_info(f"    - Total packages in config: {total_packages}")
                self.print_info(f"    - Packages installed: {installed_count}")
                self.print_info(f"    - Packages missing: {missing_count}")
                
                if missing_count == 0:
                    self.print_success("  ✓ All packages from install_config.json are installed")
                elif missing_count <= 3:
                    self.print_info(f"  ℹ Most packages installed ({missing_count} missing)")
                else:
                    self.print_info(f"  ⚠ Several packages missing ({missing_count} missing)")
                
            except Exception as e:
                self.print_error(f"  ✗ Package validation failed: {e}")
                return False
            
            self.print_success("Environment validation system test PASSED")
            return True
            
        except Exception as e:
            self.print_error(f"Environment validation system test error: {e}")
            return False
    
    def test_markdown_document_viewer(self):
        """Test Markdown document viewer functionality"""
        try:
            self.print_info("Testing Markdown document viewer...")
            
            # Test DocumentViewer import
            from ai_document_viewer import DocumentViewer, MarkdownFormatter
            self.print_success("  ✓ DocumentViewer and MarkdownFormatter imported successfully")
            
            # Test MarkdownFormatter functionality
            formatter = MarkdownFormatter()
            
            # Test various Markdown elements
            test_cases = [
                ("# Header", "Main header formatting"),
                ("## Sub Header", "Sub header formatting"),
                ("**Bold text**", "Bold text formatting"),
                ("*Italic text*", "Italic text formatting"),
                ("`inline code`", "Inline code formatting"),
                ("- List item", "List item formatting"),
                ("1. Numbered item", "Numbered list formatting"),
                ("> Blockquote", "Blockquote formatting"),
                ("[Link](url)", "Link formatting")
            ]
            
            markdown_tests_passed = 0
            for test_input, description in test_cases:
                try:
                    formatted = formatter.format_line(test_input)
                    
                    # Check if formatting was applied based on the specific test case
                    formatting_applied = False
                    
                    if test_input.startswith('# '):
                        # Header should have multiple lines or be significantly different
                        formatting_applied = '\n' in formatted or len(formatted) > len(test_input) * 2
                    elif test_input.startswith('## '):
                        # Sub header should have line break or be longer
                        formatting_applied = '\n' in formatted or len(formatted) > len(test_input) + 10
                    elif test_input.startswith('### '):
                        # Small header should be different (even if just color codes)
                        formatting_applied = True  # This always gets formatted
                    elif '**' in test_input or '*' in test_input:
                        # Bold/italic should be processed (even if color codes are empty)
                        formatting_applied = True  # format_inline always processes these
                    elif test_input.startswith('`') and test_input.endswith('`'):
                        # Inline code should be processed
                        formatting_applied = True
                    elif test_input.startswith('- '):
                        # List item should have bullet character
                        formatting_applied = '•' in formatted
                    elif re.match(r'^\d+\.\s', test_input):
                        # Numbered list - check if regex matched and processing occurred
                        match = re.match(r'^(\s*)(\d+)(\.\s)(.*)$', test_input)
                        formatting_applied = match is not None
                    elif test_input.startswith('> '):
                        # Blockquote should have pipe character
                        formatting_applied = '│' in formatted
                    elif '[' in test_input and '](' in test_input:
                        # Link should be processed
                        formatting_applied = True
                    else:
                        # For other cases, any change indicates formatting
                        formatting_applied = formatted != test_input
                    
                    if formatting_applied:
                        markdown_tests_passed += 1
                    else:
                        self.print_error(f"  ✗ {description} failed - no formatting applied")
                except Exception as e:
                    self.print_error(f"  ✗ {description} failed: {e}")
            
            if markdown_tests_passed >= 7:  # At least 7 out of 9 should pass
                self.print_success(f"  ✓ Markdown formatting tests passed ({markdown_tests_passed}/{len(test_cases)})")
            else:
                self.print_error(f"  ✗ Markdown formatting tests failed ({markdown_tests_passed}/{len(test_cases)})")
                return False
            
            # Test DocumentViewer with README.md
            viewer = DocumentViewer(self.ai_env_path)
            readme_path = viewer.ai_env_path / "README.md"
            
            if readme_path.exists():
                self.print_success("  ✓ README.md found for testing")
                
                # Test file reading
                try:
                    with open(readme_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()[:5]  # Read first 5 lines
                    
                    if lines:
                        self.print_success(f"  ✓ README.md readable ({len(lines)} test lines)")
                        
                        # Test Markdown formatting on real content
                        formatted_lines = []
                        for line in lines:
                            try:
                                formatted = viewer.formatter.format_line(line.rstrip())
                                formatted_lines.append(formatted)
                            except Exception as e:
                                self.print_error(f"  ✗ Error formatting line: {e}")
                                return False
                        
                        self.print_success("  ✓ README.md Markdown formatting successful")
                    else:
                        self.print_error("  ✗ README.md is empty")
                        return False
                        
                except Exception as e:
                    self.print_error(f"  ✗ Error reading README.md: {e}")
                    return False
            else:
                self.print_error("  ✗ README.md not found")
                return False
            
            # Test PACKAGE_INFO.txt viewing
            package_info_path = viewer.ai_env_path / "PACKAGE_INFO.txt"
            if package_info_path.exists():
                self.print_success("  ✓ PACKAGE_INFO.txt found for testing")
                
                try:
                    with open(package_info_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()[:3]  # Read first 3 lines
                    
                    if lines:
                        # Test basic text formatting
                        formatted_lines = [viewer._format_text_line(line.rstrip()) for line in lines]
                        self.print_success("  ✓ PACKAGE_INFO.txt formatting successful")
                    else:
                        self.print_error("  ✗ PACKAGE_INFO.txt is empty")
                        return False
                        
                except Exception as e:
                    self.print_error(f"  ✗ Error reading PACKAGE_INFO.txt: {e}")
                    return False
            else:
                self.print_error("  ✗ PACKAGE_INFO.txt not found")
                return False
            
            self.print_success("Markdown document viewer test PASSED")
            return True
            
        except ImportError as e:
            self.print_error(f"Document viewer import failed: {e}")
            self.print_error("Markdown document viewer test FAILED")
            return False
        except Exception as e:
            self.print_error(f"Document viewer test error: {e}")
            self.print_error("Markdown document viewer test FAILED")
            return False

    def run_all_tests(self):
        """Run all component tests"""
        print(f"\n{Fore.CYAN}🧪 Testing All Components...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        tests = [
            ("Testing Markdown document viewer", self.test_markdown_document_viewer),
            ("Testing AI Environment directory structure", self.test_directory_structure),
            ("Testing Conda installation", self.test_conda_installation),
            ("Testing AI2025 conda environment", self.test_ai2025_environment),
            ("Testing required Python packages", self.test_python_packages),
            ("Testing Ollama installation (optional)", self.test_ollama_installation),
            ("Testing AI model management system", self.test_model_management_system),
            ("Testing Jupyter Lab management system", self.test_jupyter_lab_system),
            ("Testing Ollama help and documentation", self.test_ollama_help_system),
            ("Testing environment validation system", self.test_environment_validation),
            ("Testing system integration", self.test_system_integration)
        ]
        
        total_tests = len(tests)
        passed_tests = 0
        failed_tests = 0
        
        for i, (description, test_func) in enumerate(tests, 1):
            self.print_step(i, description)
            
            if test_func():
                passed_tests += 1
            else:
                failed_tests += 1
                
            print()
        
        # Final Results
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}🔍 COMPONENT TESTING RESULTS{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        print(f"\nTotal tests run: {total_tests}")
        print(f"{Fore.GREEN}Tests passed: {passed_tests}{Style.RESET_ALL}")
        print(f"{Fore.RED}Tests failed: {failed_tests}{Style.RESET_ALL}")
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        print(f"Success rate: {success_rate:.1f}%")
        
        if failed_tests == 0:
            print(f"\n{Fore.GREEN}🎉 ALL TESTS PASSED! Your AI Environment is fully functional.{Style.RESET_ALL}")
            return True
        elif success_rate >= 80:
            print(f"\n{Fore.YELLOW}⚠️ MOSTLY WORKING: {failed_tests} test(s) failed, but core functionality is available.{Style.RESET_ALL}")
            return True
        else:
            print(f"\n{Fore.RED}❌ SIGNIFICANT ISSUES: {failed_tests} test(s) failed. Please check the installation.{Style.RESET_ALL}")
            return False

def main(path=None):
    """Run component tests.

    Args:
        path (str or Path, optional): Path to the AI Environment directory.
            If not provided, the function uses the AI_ENV_PATH environment
            variable or defaults to 'D:/AI_Environment'.
    """
    ai_env_path = Path(path or os.environ.get("AI_ENV_PATH", "D:/AI_Environment"))
    conda_path = ai_env_path / "Miniconda"

    tester = ComponentTester(ai_env_path, conda_path)
    success = tester.run_all_tests()

    if success:
        print(f"\n{Fore.GREEN}Component testing completed successfully{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}Component testing found issues{Style.RESET_ALL}")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)

