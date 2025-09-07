# AI Environment Python System v3.0.22

**Date:** 2025-08-13  
**Version:** 3.0.22  
**Description:** Modular AI development environment with interactive menus and component testing.

## Overview
This repository contains scripts and modules for managing an AI development environment.  
It includes version checking, component tests, model management, and documentation utilities.

See [docs/CHANGELOG.md](docs/CHANGELOG.md) for detailed release notes.

## File Structure
```
AI_Environment/
├── activate_ai_env.py          # Main modular script
├── check_versions.py           # Dynamic version checker (Python)
├── version_config.json         # Version configuration
├── README.md                   # Main documentation
├── docs/                       # Additional documentation
├── help/                       # Model help files
└── src/                        # Python modules
    ├── ai_component_tester/    # Component testing package
    ├── ai_menu_system.py       # Menu system
    ├── ai_action_handlers.py   # Action handlers
    ├── ai_path_manager.py      # Path management
    ├── ai_conda_manager.py     # Conda management
    ├── ai_component_setup.py   # Component setup
    ├── ai_ollama_manager.py    # Ollama management
    ├── ai_process_manager.py   # Process management
    ├── ai_app_launcher.py      # Application launcher
    ├── ai_jupyter_manager.py   # Jupyter Lab management
    ├── ai_model_manager.py     # Model management
    ├── ai_model_downloader.py  # Model downloader
    ├── ai_model_loader.py      # Model loader
    └── ai_status_display.py    # Status display
```

## Installation
1. **Extract Files**
   ```bash
   D:\AI_Environment\
   ```
2. **Check Versions**
   ```bash
   python check_versions.py
   ```
3. **Launch Environment**
   ```bash
   D:\AI_Environment\run_ai_env.bat
   ```

## Testing
*Quick Test*
```bash
run_ai_env.bat
# Select option 4 (Test All Components)
```

*Detailed Test*
```bash
run_ai_env.bat --verbose
# Select option 4 (Test All Components)
```

Sample output is available in [docs/SAMPLE_OUTPUT.md](docs/SAMPLE_OUTPUT.md).

## Available Actions
### Command Line
- `run_ai_env.bat` - Interactive menu
- `check_versions.py` - Verify file versions
- `activate_ai_env.py` - Activate environment

### Interactive Menu
1. Full Activation
2. Restore Original PATH
3. Activate Conda Environment
4. Test All Components
5. Setup Flask
6. Setup Ollama Server
7. Download AI Models
8. Run Environment Validation
9. Launch Applications
10. Background Processes
11. Advanced Options
12. Quit
13. Exit and Close All

## Troubleshooting
- **Module not found** – ensure `src` directory exists.
- **Python not found** – run Full Activation (menu option 1).
- **Conda environment not found** – verify `Miniconda` installation.

## Support
### Version Checking
```bash
python check_versions.py
```

### Additional Tests
- Use menu option **4** for system tests.
- Use `--verbose` for detailed output.

Expected result:
```
[SUCCESS] All files have correct versions (100%)
[INFO] Your AI Environment system is up to date!
```

---
**AI Environment Python System** – Advanced and Modular AI Development Environment Management System 🚀
