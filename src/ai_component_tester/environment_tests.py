import os
import subprocess

def test_directory_structure(tester):
    """Test AI Environment directory structure"""
    if tester.ai_env_path.exists():
        tester.print_success("AI Environment directory found")

        required_dirs = ["Miniconda"]
        optional_dirs = ["AI_Installer", "Ollama"]
        missing_dirs = []

        for dir_name in required_dirs:
            if (tester.ai_env_path / dir_name).exists():
                tester.print_success(f"  ✓ {dir_name} directory found")
            else:
                tester.print_error(f"  ✗ {dir_name} directory missing")
                missing_dirs.append(dir_name)

        for dir_name in optional_dirs:
            if (tester.ai_env_path / dir_name).exists():
                tester.print_success(f"  ✓ {dir_name} directory found (optional)")
            else:
                tester.print_info(f"  - {dir_name} directory not found (optional)")

        if not missing_dirs:
            tester.print_success("Directory structure test PASSED")
            return True
        tester.print_error(f"Directory structure test FAILED - Missing: {missing_dirs}")
        return False
    tester.print_error("AI Environment directory not found")
    return False


def test_conda_installation(tester):
    """Test Conda installation"""
    if tester.conda_path.exists():
        tester.print_success("Conda directory found")
        conda_exe = tester.conda_path / "Scripts" / "conda.exe"
        if conda_exe.exists():
            tester.print_success("  ✓ conda.exe found")
            try:
                result = subprocess.run([str(conda_exe), "--version"],
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    version = result.stdout.strip()
                    tester.print_success(f"  ✓ Conda version: {version}")
                    tester.print_success("Conda installation test PASSED")
                    return True
                tester.print_error("  ✗ Conda command failed")
                tester.print_error("Conda installation test FAILED")
                return False
            except Exception as e:
                tester.print_error(f"  ✗ Conda test error: {e}")
                tester.print_error("Conda installation test FAILED")
                return False
        tester.print_error("  ✗ conda.exe not found")
        tester.print_error("Conda installation test FAILED")
        return False
    tester.print_error("Conda directory not found")
    return False


def test_ai2025_environment(tester):
    """Test AI2025 conda environment"""
    ai2025_path = tester.conda_path / "envs" / "AI2025"
    if ai2025_path.exists():
        tester.print_success("AI2025 environment directory found")
        python_exe = ai2025_path / "python.exe"
        if python_exe.exists():
            tester.print_success("  ✓ Python executable found")
            try:
                result = subprocess.run([str(python_exe), "--version"],
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    version = result.stdout.strip()
                    tester.print_success(f"  ✓ Python version: {version}")
                    tester.print_success("AI2025 environment test PASSED")
                    return True
                tester.print_error("  ✗ Python version check failed")
                tester.print_error("AI2025 environment test FAILED")
                return False
            except Exception as e:
                tester.print_error(f"  ✗ Python test error: {e}")
                tester.print_error("AI2025 environment test FAILED")
                return False
        tester.print_error("  ✗ Python executable not found")
        tester.print_error("AI2025 environment test FAILED")
        return False
    tester.print_error("AI2025 environment not found")
    return False
