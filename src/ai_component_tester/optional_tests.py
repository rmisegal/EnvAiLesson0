import os
import subprocess

from ai_path_manager import PathManager


def test_ollama_installation(tester):
    """Test Ollama installation (optional)"""
    ollama_path = tester.ai_env_path / "Ollama"
    if ollama_path.exists():
        tester.print_success("Ollama directory found")
        ollama_exe = ollama_path / "ollama.exe"
        if ollama_exe.exists():
            tester.print_success("  ✓ ollama.exe found")
            try:
                result = subprocess.run([str(ollama_exe), "version"],
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    tester.print_success(
                        f"  ✓ Ollama version: {result.stdout.strip()}"
                    )
                    tester.print_success("Ollama installation test PASSED")
                    return True
                tester.print_info(
                    "  - Version command failed, trying alternative check..."
                )
                result2 = subprocess.run([str(ollama_exe), "--help"],
                                        capture_output=True, text=True, timeout=5)
                if result2.returncode == 0:
                    tester.print_success(
                        "  ✓ Ollama executable responds to --help"
                    )
                    tester.print_success(
                        "Ollama installation test PASSED (basic)"
                    )
                    return True
                tester.print_error(
                    f"  ✗ Ollama version check failed (exit code: {result.returncode})"
                )
                if result.stderr:
                    tester.print_error(
                        f"  ✗ Error output: {result.stderr.strip()}"
                    )
                tester.print_error("Ollama installation test FAILED")
                return False
            except Exception as e:
                tester.print_error(f"  ✗ Ollama test error: {e}")
                tester.print_error("Ollama installation test FAILED")
                return False
        tester.print_error("  ✗ ollama.exe not found")
        tester.print_error("Ollama installation test FAILED")
        return False
    tester.print_info("Ollama not installed (optional component)")
    return True


def test_model_management_system(tester):
    """Test AI model management components"""
    try:
        tester.print_info("Testing AI model management system...")
        try:
            import sys
            sys.path.append(str(tester.ai_env_path / "src"))
            from ai_model_manager import AIModelManager
            tester.print_success("  ✓ AI Model Manager module loads correctly")
        except ImportError as e:
            tester.print_error(f"  ✗ AI Model Manager import failed: {e}")
            return False
        try:
            from ai_model_loader import ModelLoader
            tester.print_success("  ✓ Model Loader module loads correctly")
        except ImportError as e:
            tester.print_error(f"  ✗ Model Loader import failed: {e}")
            return False
        try:
            from ai_model_downloader import ModelDownloader
            tester.print_success("  ✓ Model Downloader module loads correctly")
        except ImportError as e:
            tester.print_error(f"  ✗ Model Downloader import failed: {e}")
            return False
        help_dir = tester.ai_env_path / "help"
        if help_dir.exists():
            help_files = list(help_dir.glob("*.txt"))
            if len(help_files) >= 5:
                tester.print_success(
                    f"  ✓ Help directory contains {len(help_files)} model help files"
                )
            else:
                tester.print_warning(
                    f"  ⚠ Help directory contains only {len(help_files)} files (expected 5+)"
                )
        else:
            tester.print_error("  ✗ Help directory not found")
            return False
        tester.print_success("Model management system test PASSED")
        return True
    except Exception as e:
        tester.print_error(f"Model management system test error: {e}")
        return False


def test_jupyter_lab_system(tester):
    """Test Jupyter Lab management components"""
    try:
        tester.print_info("Testing Jupyter Lab management system...")
        try:
            import sys
            sys.path.append(str(tester.ai_env_path / "src"))
            from ai_jupyter_manager import JupyterLabManager
            tester.print_success("  ✓ Jupyter Lab Manager module loads correctly")
        except ImportError as e:
            tester.print_error(f"  ✗ Jupyter Lab Manager import failed: {e}")
            return False
        projects_dir = tester.ai_env_path / "Projects"
        if projects_dir.exists():
            project_dirs = [d for d in projects_dir.iterdir() if d.is_dir()]
            if len(project_dirs) > 0:
                tester.print_success(
                    f"  ✓ Projects directory contains {len(project_dirs)} project(s)"
                )
            else:
                tester.print_info(
                    "  ℹ Projects directory is empty (normal for new installation)"
                )
        else:
            tester.print_info(
                "  ℹ Projects directory not found (will be created when needed)"
            )
        basic_example = tester.ai_env_path / "Projects" / "01_Basic_LLM_Example"
        if basic_example.exists():
            if (basic_example / "main.py").exists():
                tester.print_success("  ✓ Basic LLM Example project found")
            else:
                tester.print_info("  ℹ Basic LLM Example main.py not found")
        else:
            tester.print_info("  ℹ Basic LLM Example project not found")
        tester.print_success("Jupyter Lab system test PASSED")
        return True
    except Exception as e:
        tester.print_error(f"Jupyter Lab system test error: {e}")
        return False


def test_ollama_help_system(tester):
    """Test Ollama help and documentation system"""
    try:
        tester.print_info("Testing Ollama help system...")
        help_dir = tester.ai_env_path / "help"
        if not help_dir.exists():
            tester.print_error("  ✗ Help directory not found")
            return False
        expected_help_files = [
            "phi_2_7b.txt",
            "llama2_7b.txt",
            "mistral_7b.txt",
            "codellama_7b.txt",
            "gpt_oss_20b.txt",
        ]
        found_files = 0
        for help_file in expected_help_files:
            file_path = help_dir / help_file
            if file_path.exists():
                if file_path.stat().st_size > 100:
                    tester.print_success(
                        f"  ✓ {help_file} found and has content"
                    )
                    found_files += 1
                else:
                    tester.print_warning(
                        f"  ⚠ {help_file} found but appears empty"
                    )
            else:
                tester.print_error(f"  ✗ {help_file} not found")
        if found_files >= 4:
            tester.print_success(
                f"Ollama help system test PASSED ({found_files}/5 files)"
            )
            return True
        tester.print_error(
            f"Ollama help system test FAILED ({found_files}/5 files)"
        )
        return False
    except Exception as e:
        tester.print_error(f"Ollama help system test error: {e}")
        return False


def test_system_integration(tester):
    """Test system integration"""
    try:
        current_path = os.environ.get('PATH', '')
        if 'AI_Environment' in current_path:
            tester.print_success("  ✓ AI Environment paths in system PATH")
        else:
            tester.print_info("  ℹ AI Environment paths not in current PATH (normal)")
        conda_env = os.environ.get('CONDA_DEFAULT_ENV', '')
        if conda_env:
            tester.print_success(f"  ✓ Active conda environment: {conda_env}")
        else:
            tester.print_info("  ℹ No active conda environment")
        path_manager = PathManager()
        cmd_results = path_manager.test_basic_commands()
        working_commands = sum(1 for result in cmd_results.values() if result)
        total_commands = len(cmd_results)
        if working_commands == total_commands:
            tester.print_success(
                f"  ✓ All Windows commands working ({working_commands}/{total_commands})"
            )
            tester.print_success("System integration test PASSED")
            return True
        tester.print_error(
            f"  ✗ Some Windows commands not working ({working_commands}/{total_commands})"
        )
        tester.print_error("System integration test FAILED")
        return False
    except Exception as e:
        tester.print_error(f"System integration test error: {e}")
        return False
