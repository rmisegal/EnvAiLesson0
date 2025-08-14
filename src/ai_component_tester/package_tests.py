import subprocess

from ai_conda_manager import CondaManager
from ai_environment_validator import EnvironmentValidator


def test_python_packages(tester):
    """Test required Python packages"""
    required_packages = ["psutil", "colorama", "requests", "numpy", "pandas"]
    try:
        conda_manager = CondaManager(tester.conda_path)
        conda_manager.setup_conda_paths("AI2025")
        package_results = []
        for package in required_packages:
            try:
                if package == "pandas":
                    timeout_duration = 15
                    tester.print_info(f"  Testing {package} (may take a moment)...")
                elif package == "numpy":
                    timeout_duration = 10
                    tester.print_info(f"  Testing {package} (may take a moment)...")
                else:
                    timeout_duration = 5
                result = subprocess.run([
                    "python", "-c", f"import {package}; print('{package} OK')"
                ], capture_output=True, text=True, timeout=timeout_duration)
                if result.returncode == 0:
                    tester.print_success(f"  ✓ {package} package available")
                    package_results.append(True)
                else:
                    tester.print_error(f"  ✗ {package} package missing or broken")
                    package_results.append(False)
            except subprocess.TimeoutExpired:
                tester.print_error(
                    f"  ✗ {package} test error: command timed out after {timeout_duration} seconds"
                )
                package_results.append(False)
            except Exception as e:
                tester.print_error(f"  ✗ {package} test error: {e}")
                package_results.append(False)
        if all(package_results):
            tester.print_success("Python packages test PASSED")
            return True
        missing_count = len([r for r in package_results if not r])
        tester.print_error(
            f"Python packages test FAILED - {missing_count}/{len(required_packages)} packages missing"
        )
        return False
    except Exception as e:
        tester.print_error(f"Package testing failed: {e}")
        return False


def test_environment_validation(tester):
    """Test environment validation system"""
    try:
        tester.print_info("Testing environment validation system...")
        config_dir = tester.ai_env_path / "config"
        if not config_dir.exists():
            tester.print_error("  ✗ Config directory not found")
            return False
        tester.print_success("  ✓ Config directory found")
        config_file = config_dir / "install_config.json"
        if not config_file.exists():
            tester.print_error("  ✗ install_config.json not found")
            return False
        tester.print_success("  ✓ install_config.json found")
        try:
            validator = EnvironmentValidator(tester.ai_env_path)
            if validator.load_config():
                tester.print_success("  ✓ Configuration loaded successfully")
            else:
                tester.print_error("  ✗ Failed to load configuration")
                return False
        except Exception as e:
            tester.print_error(f"  ✗ Validator initialization failed: {e}")
            return False
        try:
            tester.print_info(
                "  Performing package validation against install_config.json..."
            )
            validator.check_python_packages()
            total_packages = len(validator.config.get('python_packages', []))
            installed_count = len(validator.installed_packages)
            missing_count = len(validator.missing_packages)
            tester.print_success("  ✓ Package validation completed")
            tester.print_info(f"    - Total packages in config: {total_packages}")
            tester.print_info(f"    - Packages installed: {installed_count}")
            tester.print_info(f"    - Packages missing: {missing_count}")
            if missing_count == 0:
                tester.print_success(
                    "  ✓ All packages from install_config.json are installed"
                )
            elif missing_count <= 3:
                tester.print_info(
                    f"  ℹ Most packages installed ({missing_count} missing)"
                )
            else:
                tester.print_info(
                    f"  ⚠ Several packages missing ({missing_count} missing)"
                )
        except Exception as e:
            tester.print_error(f"  ✗ Package validation failed: {e}")
            return False
        tester.print_success("Environment validation system test PASSED")
        return True
    except Exception as e:
        tester.print_error(f"Environment validation system test error: {e}")
        return False
