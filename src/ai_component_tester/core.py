from pathlib import Path

try:
    from colorama import Fore, Style
except ImportError:
    class Fore:
        GREEN = RED = YELLOW = CYAN = BLUE = ""
    class Style:
        RESET_ALL = ""

from .environment_tests import (
    test_directory_structure,
    test_conda_installation,
    test_ai2025_environment,
)
from .package_tests import test_python_packages, test_environment_validation
from .optional_tests import (
    test_ollama_installation,
    test_model_management_system,
    test_jupyter_lab_system,
    test_ollama_help_system,
    test_system_integration,
)
from .markdown_viewer_test import test_markdown_document_viewer


class ComponentTester:
    """Comprehensive testing of AI Environment components"""

    def __init__(self, ai_env_path, conda_path):
        self.ai_env_path = Path(ai_env_path)
        self.conda_path = Path(conda_path)

    def print_step(self, step_num, description):
        print(f"{Fore.CYAN}[*] Step {step_num}: {description}...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'-'*50}{Style.RESET_ALL}")

    def print_success(self, message):
        print(f"{Fore.GREEN}[OK] {message}{Style.RESET_ALL}")

    def print_error(self, message):
        print(f"{Fore.RED}[ERROR] {message}{Style.RESET_ALL}")

    def print_info(self, message):
        print(f"{Fore.YELLOW}[INFO] {message}{Style.RESET_ALL}")

    def print_warning(self, message):
        print(f"{Fore.YELLOW}[WARNING] {message}{Style.RESET_ALL}")

    def run_all_tests(self):
        print(f"\n{Fore.CYAN}🧪 Testing All Components...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        tests = [
            ("Testing Markdown document viewer", test_markdown_document_viewer),
            ("Testing AI Environment directory structure", test_directory_structure),
            ("Testing Conda installation", test_conda_installation),
            ("Testing AI2025 conda environment", test_ai2025_environment),
            ("Testing required Python packages", test_python_packages),
            ("Testing Ollama installation (optional)", test_ollama_installation),
            ("Testing AI model management system", test_model_management_system),
            ("Testing Jupyter Lab management system", test_jupyter_lab_system),
            ("Testing Ollama help and documentation", test_ollama_help_system),
            ("Testing environment validation system", test_environment_validation),
            ("Testing system integration", test_system_integration),
        ]
        total_tests = len(tests)
        passed_tests = 0
        failed_tests = 0
        for i, (description, test_func) in enumerate(tests, 1):
            self.print_step(i, description)
            if test_func(self):
                passed_tests += 1
            else:
                failed_tests += 1
            print()
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}🔍 COMPONENT TESTING RESULTS{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"\nTotal tests run: {total_tests}")
        print(f"{Fore.GREEN}Tests passed: {passed_tests}{Style.RESET_ALL}")
        print(f"{Fore.RED}Tests failed: {failed_tests}{Style.RESET_ALL}")
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        print(f"Success rate: {success_rate:.1f}%")
        if failed_tests == 0:
            print(
                f"\n{Fore.GREEN}🎉 ALL TESTS PASSED! Your AI Environment is fully functional.{Style.RESET_ALL}"
            )
            return True
        elif success_rate >= 80:
            print(
                f"\n{Fore.YELLOW}⚠️ MOSTLY WORKING: {failed_tests} test(s) failed, but core functionality is available.{Style.RESET_ALL}"
            )
            return True
        else:
            print(
                f"\n{Fore.RED}❌ SIGNIFICANT ISSUES: {failed_tests} test(s) failed. Please check the installation.{Style.RESET_ALL}"
            )
            return False


def main():
    """Test component tester"""
    ai_env_path = Path("D:/AI_Environment")
    conda_path = ai_env_path / "Miniconda"
    tester = ComponentTester(ai_env_path, conda_path)
    success = tester.run_all_tests()
    if success:
        print(f"\n{Fore.GREEN}Component testing completed successfully{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}Component testing found issues{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
