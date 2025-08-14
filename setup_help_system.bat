@echo off
title AI Environment Help System Setup

echo.
echo ================================================================
echo           AI Environment Help System Setup
echo ================================================================
echo.
echo This script will create the help system in your AI Environment.
echo.
echo Target location: D:\AI_Environment\help\
echo.

:: Check if AI Environment exists
if not exist "D:\AI_Environment" (
    echo ERROR: AI Environment not found at D:\AI_Environment
    echo Please ensure your AI Environment is installed first.
    pause
    exit /b 1
)

:: Create help directory
echo Creating help directory...
if not exist "D:\AI_Environment\help" mkdir "D:\AI_Environment\help"

echo.
echo Creating help files...

:: Create help_menu.bat
echo [1/9] Creating help menu system...
echo @echo off > "D:\AI_Environment\help\help_menu.bat"
echo title AI Environment Help System >> "D:\AI_Environment\help\help_menu.bat"
echo. >> "D:\AI_Environment\help\help_menu.bat"
echo set "HELP_DIR=%%~dp0" >> "D:\AI_Environment\help\help_menu.bat"
echo. >> "D:\AI_Environment\help\help_menu.bat"
echo :main_menu >> "D:\AI_Environment\help\help_menu.bat"
echo cls >> "D:\AI_Environment\help\help_menu.bat"
echo echo. >> "D:\AI_Environment\help\help_menu.bat"
echo echo ================================================================ >> "D:\AI_Environment\help\help_menu.bat"
echo echo                  AI Environment Help System >> "D:\AI_Environment\help\help_menu.bat"
echo echo ================================================================ >> "D:\AI_Environment\help\help_menu.bat"
echo echo. >> "D:\AI_Environment\help\help_menu.bat"
echo echo Select a help topic: >> "D:\AI_Environment\help\help_menu.bat"
echo echo. >> "D:\AI_Environment\help\help_menu.bat"
echo echo  1. Using Ollama AI Models >> "D:\AI_Environment\help\help_menu.bat"
echo echo  2. Using VS Code with AI Environment >> "D:\AI_Environment\help\help_menu.bat"
echo echo  3. Python Development >> "D:\AI_Environment\help\help_menu.bat"
echo echo  4. Project Examples >> "D:\AI_Environment\help\help_menu.bat"
echo echo  5. Managing Ollama Server >> "D:\AI_Environment\help\help_menu.bat"
echo echo  6. Environment Management >> "D:\AI_Environment\help\help_menu.bat"
echo echo  7. Shutdown Procedures >> "D:\AI_Environment\help\help_menu.bat"
echo echo  8. Useful Tips and Troubleshooting >> "D:\AI_Environment\help\help_menu.bat"
echo echo. >> "D:\AI_Environment\help\help_menu.bat"
echo echo  9. Show All Topics ^(Full Guide^) >> "D:\AI_Environment\help\help_menu.bat"
echo echo  0. Exit Help System >> "D:\AI_Environment\help\help_menu.bat"
echo echo. >> "D:\AI_Environment\help\help_menu.bat"
echo echo ================================================================ >> "D:\AI_Environment\help\help_menu.bat"
echo echo. >> "D:\AI_Environment\help\help_menu.bat"
echo set /p choice="Enter your choice (0-9): " >> "D:\AI_Environment\help\help_menu.bat"
echo. >> "D:\AI_Environment\help\help_menu.bat"
echo if "%%choice%%"=="1" call :show_help "1_ollama_models.txt" >> "D:\AI_Environment\help\help_menu.bat"
echo if "%%choice%%"=="2" call :show_help "2_vscode_usage.txt" >> "D:\AI_Environment\help\help_menu.bat"
echo if "%%choice%%"=="3" call :show_help "3_python_development.txt" >> "D:\AI_Environment\help\help_menu.bat"
echo if "%%choice%%"=="4" call :show_help "4_project_examples.txt" >> "D:\AI_Environment\help\help_menu.bat"
echo if "%%choice%%"=="5" call :show_help "5_manage_ollama.txt" >> "D:\AI_Environment\help\help_menu.bat"
echo if "%%choice%%"=="6" call :show_help "6_environment_management.txt" >> "D:\AI_Environment\help\help_menu.bat"
echo if "%%choice%%"=="7" call :show_help "7_shutdown_procedures.txt" >> "D:\AI_Environment\help\help_menu.bat"
echo if "%%choice%%"=="8" call :show_help "8_useful_tips.txt" >> "D:\AI_Environment\help\help_menu.bat"
echo if "%%choice%%"=="9" call :show_all_help >> "D:\AI_Environment\help\help_menu.bat"
echo if "%%choice%%"=="0" goto :exit_help >> "D:\AI_Environment\help\help_menu.bat"
echo. >> "D:\AI_Environment\help\help_menu.bat"
echo echo. >> "D:\AI_Environment\help\help_menu.bat"
echo echo Invalid choice. Please try again. >> "D:\AI_Environment\help\help_menu.bat"
echo pause >> "D:\AI_Environment\help\help_menu.bat"
echo goto :main_menu >> "D:\AI_Environment\help\help_menu.bat"
echo. >> "D:\AI_Environment\help\help_menu.bat"
echo :show_help >> "D:\AI_Environment\help\help_menu.bat"
echo cls >> "D:\AI_Environment\help\help_menu.bat"
echo echo. >> "D:\AI_Environment\help\help_menu.bat"
echo echo ================================================================ >> "D:\AI_Environment\help\help_menu.bat"
echo echo                     AI Environment Help >> "D:\AI_Environment\help\help_menu.bat"
echo echo ================================================================ >> "D:\AI_Environment\help\help_menu.bat"
echo echo. >> "D:\AI_Environment\help\help_menu.bat"
echo if exist "%%HELP_DIR%%%%~1" ^( >> "D:\AI_Environment\help\help_menu.bat"
echo     type "%%HELP_DIR%%%%~1" >> "D:\AI_Environment\help\help_menu.bat"
echo ^) else ^( >> "D:\AI_Environment\help\help_menu.bat"
echo     echo ERROR: Help file "%%~1" not found. >> "D:\AI_Environment\help\help_menu.bat"
echo     echo Please ensure all help files are in the help directory. >> "D:\AI_Environment\help\help_menu.bat"
echo ^) >> "D:\AI_Environment\help\help_menu.bat"
echo echo. >> "D:\AI_Environment\help\help_menu.bat"
echo echo ================================================================ >> "D:\AI_Environment\help\help_menu.bat"
echo echo. >> "D:\AI_Environment\help\help_menu.bat"
echo pause >> "D:\AI_Environment\help\help_menu.bat"
echo goto :main_menu >> "D:\AI_Environment\help\help_menu.bat"
echo. >> "D:\AI_Environment\help\help_menu.bat"
echo :show_all_help >> "D:\AI_Environment\help\help_menu.bat"
echo cls >> "D:\AI_Environment\help\help_menu.bat"
echo echo. >> "D:\AI_Environment\help\help_menu.bat"
echo echo ================================================================ >> "D:\AI_Environment\help\help_menu.bat"
echo echo                   COMPLETE AI ENVIRONMENT GUIDE >> "D:\AI_Environment\help\help_menu.bat"
echo echo ================================================================ >> "D:\AI_Environment\help\help_menu.bat"
echo echo. >> "D:\AI_Environment\help\help_menu.bat"
echo. >> "D:\AI_Environment\help\help_menu.bat"
echo for %%%%f in ^("%%HELP_DIR%%*.txt"^) do ^( >> "D:\AI_Environment\help\help_menu.bat"
echo     echo. >> "D:\AI_Environment\help\help_menu.bat"
echo     echo ---------------------------------------------------------------- >> "D:\AI_Environment\help\help_menu.bat"
echo     type "%%%%f" >> "D:\AI_Environment\help\help_menu.bat"
echo     echo ---------------------------------------------------------------- >> "D:\AI_Environment\help\help_menu.bat"
echo ^) >> "D:\AI_Environment\help\help_menu.bat"
echo. >> "D:\AI_Environment\help\help_menu.bat"
echo echo. >> "D:\AI_Environment\help\help_menu.bat"
echo echo ================================================================ >> "D:\AI_Environment\help\help_menu.bat"
echo echo                     End of Complete Guide >> "D:\AI_Environment\help\help_menu.bat"
echo echo ================================================================ >> "D:\AI_Environment\help\help_menu.bat"
echo echo. >> "D:\AI_Environment\help\help_menu.bat"
echo pause >> "D:\AI_Environment\help\help_menu.bat"
echo goto :main_menu >> "D:\AI_Environment\help\help_menu.bat"
echo. >> "D:\AI_Environment\help\help_menu.bat"
echo :exit_help >> "D:\AI_Environment\help\help_menu.bat"
echo echo. >> "D:\AI_Environment\help\help_menu.bat"
echo echo Exiting Help System... >> "D:\AI_Environment\help\help_menu.bat"
echo exit /b 0 >> "D:\AI_Environment\help\help_menu.bat"

:: Create 1_ollama_models.txt
echo [2/9] Creating Ollama models help...
(
echo USING OLLAMA AI MODELS
echo ================================================================
echo.
echo BASIC COMMANDS:
echo ----------------------------------------------------------------
echo List available models:
echo   ollama list
echo.
echo Download new models:
echo   ollama pull llama2:7b
echo   ollama pull codellama:7b
echo   ollama pull mistral:7b
echo   ollama pull phi:2.7b
echo.
echo Start interactive chat with a model:
echo   ollama run llama2
echo   ollama run codellama      ^(for coding assistance^)
echo   ollama run mistral        ^(for general AI tasks^)
echo   ollama run phi            ^(lightweight, fast model^)
echo.
echo Exit chat: Type /bye or press Ctrl+C
echo.
echo AVAILABLE MODELS:
echo ----------------------------------------------------------------
echo - llama2:7b     - General purpose conversational AI
echo - codellama:7b  - Specialized for code generation and help
echo - mistral:7b    - Efficient general purpose model
echo - phi:2.7b      - Compact high-performance model
echo.
echo MODEL USAGE TIPS:
echo ----------------------------------------------------------------
echo - First time loading a model may take 1-2 minutes
echo - Models stay in memory for faster subsequent use
echo - Use codellama for programming questions
echo - Use llama2 or mistral for general questions
echo - phi model is fastest for quick responses
echo.
echo EXAMPLE CHAT SESSION:
echo ----------------------------------------------------------------
echo ^> ollama run llama2
echo ^>^>^> Hello, can you help me learn Python?
echo Sure! Python is a great language for AI and data science...
echo.
echo ^>^>^> How do I use pandas for data analysis?
echo Pandas is excellent for data manipulation. Here's how...
echo.
echo ^>^>^> /bye
echo Goodbye!
echo.
echo API USAGE ^(for developers^):
echo ----------------------------------------------------------------
echo Ollama provides a REST API at: http://127.0.0.1:11434
echo.
echo Python example:
echo import requests
echo response = requests.post^('http://127.0.0.1:11434/api/generate', 
echo     json={'model': 'llama2', 'prompt': 'Hello!', 'stream': False}^)
echo print^(response.json^(^)['response']^)
) > "D:\AI_Environment\help\1_ollama_models.txt"

:: Create 2_vscode_usage.txt
echo [3/9] Creating VS Code usage help...
(
echo USING VS CODE WITH AI ENVIRONMENT
echo ================================================================
echo.
echo OPENING VS CODE:
echo ----------------------------------------------------------------
echo Open VS Code in current directory:
echo   code .
echo.
echo Open VS Code in Projects folder:
echo   cd Projects
echo   code .
echo.
echo Open specific file:
echo   code filename.py
echo.
echo WHAT'S PRE-CONFIGURED:
echo ----------------------------------------------------------------
echo - Python interpreter: AI2025 environment automatically selected
echo - Jupyter notebook support built-in
echo - Python extensions installed:
echo   * Python language support
echo   * Jupyter integration
echo   * Python linting and formatting
echo   * Code debugging
echo - AI development settings optimized
echo.
echo CREATING NEW PROJECTS:
echo ----------------------------------------------------------------
echo 1. Navigate to Projects folder:
echo    cd Projects
echo.
echo 2. Create new project folder:
echo    mkdir MyAIProject
echo    cd MyAIProject
echo.
echo 3. Open in VS Code:
echo    code .
echo.
echo 4. Create new Python file:
echo    File ^> New File
echo    Save as: main.py
echo.
echo 5. Start coding with AI libraries!
echo.
echo USEFUL VS CODE FEATURES:
echo ----------------------------------------------------------------
echo - Ctrl+Shift+P: Command palette
echo - F5: Run/Debug Python script
echo - Ctrl+Enter: Run code in Python terminal
echo - Shift+Enter: Run code in Jupyter cell
echo.
echo JUPYTER NOTEBOOKS IN VS CODE:
echo ----------------------------------------------------------------
echo 1. Create new notebook:
echo    File ^> New File
echo    Save as: notebook.ipynb
echo.
echo 2. Select kernel:
echo    Click "Select Kernel" ^> AI2025 environment
echo.
echo 3. Write code in cells and run with Shift+Enter
echo.
echo PYTHON DEBUGGING:
echo ----------------------------------------------------------------
echo - Set breakpoints: Click left margin next to line numbers
echo - Press F5 to start debugging
echo - F10: Step over, F11: Step into, F5: Continue
echo.
echo INTEGRATED TERMINAL:
echo ----------------------------------------------------------------
echo - Terminal ^> New Terminal
echo - Automatically activates AI2025 environment
echo - Run commands directly: python, pip, ollama, etc.
echo.
echo WORKSPACE SETTINGS:
echo ----------------------------------------------------------------
echo VS Code is configured to:
echo - Use Python from D:\AI_Environment\Miniconda\envs\AI2025
echo - Enable auto-completion for AI libraries
echo - Format code with Black formatter
echo - Lint code with pylint
) > "D:\AI_Environment\help\2_vscode_usage.txt"

:: Create remaining help files (3-8)...
echo [4/9] Creating Python development help...
(
echo PYTHON DEVELOPMENT
echo ================================================================
echo.
echo BASIC PYTHON COMMANDS:
echo ----------------------------------------------------------------
echo Start Python interpreter:
echo   python
echo.
echo Run Python scripts:
echo   python your_script.py
echo   python -m script_name
echo.
echo Check Python version:
echo   python --version
echo.
echo Exit Python interpreter:
echo   exit^(^) or Ctrl+Z then Enter
echo.
echo JUPYTER LAB:
echo ----------------------------------------------------------------
echo Start Jupyter Lab:
echo   jupyter lab
echo.
echo This opens in your web browser at: http://localhost:8888
echo.
echo Features:
echo - Interactive notebooks ^(.ipynb files^)
echo - File browser and editor
echo - Terminal access
echo - Variable inspector
echo - Markdown support
echo.
echo PACKAGE MANAGEMENT:
echo ----------------------------------------------------------------
echo Install new packages:
echo   pip install package-name
echo.
echo Install specific version:
echo   pip install package-name==1.2.3
echo.
echo List installed packages:
echo   pip list
echo   conda list
echo.
echo Update package:
echo   pip install --upgrade package-name
echo.
echo Uninstall package:
echo   pip uninstall package-name
echo.
echo PRE-INSTALLED AI LIBRARIES:
echo ----------------------------------------------------------------
echo Core AI Frameworks:
echo - langchain      - LLM application framework
echo - langgraph      - Graph-based AI workflows  
echo - pyautogen      - Multi-agent conversations
echo - transformers   - Hugging Face models
echo - torch          - PyTorch deep learning
echo.
echo Web Frameworks:
echo - streamlit      - AI web apps
echo - fastapi        - REST APIs
echo - gradio         - ML interfaces
echo - flask          - Web development
echo.
echo Data Science:
echo - pandas         - Data manipulation
echo - numpy          - Numerical computing
echo - matplotlib     - Plotting
echo - seaborn        - Statistical visualization
echo - plotly         - Interactive plots
echo - scikit-learn   - Machine learning
echo.
echo Development Tools:
echo - jupyter        - Interactive development
echo - black          - Code formatting
echo - pylint         - Code linting
echo - requests       - HTTP requests
echo.
echo EXAMPLE AI SCRIPT:
echo ----------------------------------------------------------------
echo # Simple AI chat with Ollama
echo import requests
echo import json
echo.
echo def chat_with_ai^(message^):
echo     url = "http://127.0.0.1:11434/api/generate"
echo     data = {
echo         "model": "llama2",
echo         "prompt": message,
echo         "stream": False
echo     }
echo     response = requests.post^(url, json=data^)
echo     return response.json^(^)["response"]
echo.
echo # Use it
echo response = chat_with_ai^("Hello, how are you?"^)
echo print^(response^)
echo.
echo VIRTUAL ENVIRONMENT INFO:
echo ----------------------------------------------------------------
echo Current environment: AI2025
echo Location: D:\AI_Environment\Miniconda\envs\AI2025
echo Python executable: D:\AI_Environment\Miniconda\envs\AI2025\python.exe
echo.
echo Always ensure you're in the AI2025 environment for AI development!
) > "D:\AI_Environment\help\3_python_development.txt"

echo [5/9] Creating project examples help...
(
echo PROJECT EXAMPLES
echo ================================================================
echo.
echo NAVIGATING TO EXAMPLES:
echo ----------------------------------------------------------------
echo Go to Projects folder:
echo   cd Projects
echo.
echo List available examples:
echo   dir
echo.
echo View project structure:
echo   tree /f
echo.
echo AVAILABLE PROJECT TEMPLATES:
echo ----------------------------------------------------------------
echo.
echo 1. 01_Basic_LLM_Example
echo    Description: Simple Ollama integration
echo    File: main.py
echo    Run with: python main.py
echo    
echo    What it demonstrates:
echo    - Direct HTTP requests to Ollama API
echo    - Basic prompt and response handling
echo    - Error handling for API calls
echo.
echo 2. 02_LangChain_Example
echo    Description: LangChain framework demo
echo    File: main.py
echo    Run with: python main.py
echo    
echo    What it demonstrates:
echo    - LangChain LLM integration
echo    - Prompt templates
echo    - Chain creation and execution
echo.
echo 3. 03_Streamlit_App
echo    Description: Web AI chat interface
echo    File: app.py
echo    Run with: streamlit run app.py
echo    
echo    What it demonstrates:
echo    - Web-based chat interface
echo    - Model selection
echo    - Session state management
echo    - Real-time AI responses
echo.
echo RUNNING THE EXAMPLES:
echo ----------------------------------------------------------------
echo.
echo Basic LLM Example:
echo   cd Projects\01_Basic_LLM_Example
echo   python main.py
echo.
echo LangChain Example:
echo   cd Projects\02_LangChain_Example
echo   python main.py
echo.
echo Streamlit Web App:
echo   cd Projects\03_Streamlit_App
echo   streamlit run app.py
echo   ^(Opens in browser at http://localhost:8501^)
echo.
echo CREATING YOUR OWN PROJECTS:
echo ----------------------------------------------------------------
echo.
echo 1. Create new project folder:
echo    cd Projects
echo    mkdir MyNewProject
echo    cd MyNewProject
echo.
echo 2. Create main Python file:
echo    echo. ^> main.py
echo.
echo 3. Open in VS Code:
echo    code .
echo.
echo 4. Start with basic template:
echo    # My AI Project
echo    import requests
echo    import json
echo    
echo    # Your code here
echo.
echo The AI environment is portable, so your projects work anywhere!
) > "D:\AI_Environment\help\4_project_examples.txt"

echo [6/9] Creating Ollama management help...
(
echo MANAGING OLLAMA SERVER
echo ================================================================
echo.
echo SERVER STATUS:
echo ----------------------------------------------------------------
echo Check if Ollama is running:
echo   tasklist ^| findstr ollama
echo.
echo Check Ollama version:
echo   ollama --version
echo.
echo View server logs:
echo   Look for ollama.exe process in Task Manager
echo.
echo SERVER CONTROL:
echo ----------------------------------------------------------------
echo Start Ollama server manually:
echo   ollama serve
echo.
echo Start Ollama in background:
echo   start /B ollama serve
echo.
echo Stop Ollama server:
echo   taskkill /IM ollama.exe /F
echo.
echo Restart Ollama server:
echo   taskkill /IM ollama.exe /F ^&^& ollama serve
echo.
echo SERVER CONFIGURATION:
echo ----------------------------------------------------------------
echo Default API endpoint: http://127.0.0.1:11434
echo Models directory: D:\AI_Environment\Models
echo Config location: D:\AI_Environment\Ollama
echo.
echo Environment variables ^(automatically set^):
echo - OLLAMA_HOST=127.0.0.1:11434
echo - OLLAMA_MODELS=D:\AI_Environment\Models
echo.
echo TROUBLESHOOTING:
echo ----------------------------------------------------------------
echo.
echo Problem: "connection refused" errors
echo Solution: 
echo   1. Check if Ollama is running: tasklist ^| findstr ollama
echo   2. If not running: ollama serve
echo   3. Wait 10-15 seconds for startup
echo.
echo Problem: Models not found
echo Solution:
echo   1. Check models: ollama list
echo   2. Download missing model: ollama pull llama2
echo   3. Verify model location: dir D:\AI_Environment\Models
echo.
echo Problem: Slow responses
echo Solution:
echo   1. Check available RAM
echo   2. Close unnecessary applications
echo   3. Use smaller models ^(phi instead of llama2^)
echo   4. Restart Ollama: taskkill /IM ollama.exe /F ^&^& ollama serve
echo.
echo MODEL MANAGEMENT:
echo ----------------------------------------------------------------
echo List all models:
echo   ollama list
echo.
echo Remove unused models:
echo   ollama rm model-name
echo.
echo Pull new models:
echo   ollama pull model-name
echo.
echo Copy models between installations:
echo   - Copy files from D:\AI_Environment\Models
echo   - Run "ollama list" to verify
) > "D:\AI_Environment\help\5_manage_ollama.txt"

echo [7/9] Creating environment management help...
(
echo ENVIRONMENT MANAGEMENT
echo ================================================================
echo.
echo CONDA ENVIRONMENT BASICS:
echo ----------------------------------------------------------------
echo Check current environment:
echo   echo %%CONDA_DEFAULT_ENV%%
echo.
echo List all environments:
echo   conda env list
echo.
echo Activate AI2025 environment:
echo   conda activate AI2025
echo.
echo Deactivate current environment:
echo   conda deactivate
echo.
echo PACKAGE MANAGEMENT:
echo ----------------------------------------------------------------
echo List installed packages:
echo   conda list
echo   pip list
echo.
echo Install packages:
echo   conda install package-name
echo   pip install package-name
echo.
echo Update packages:
echo   conda update package-name
echo   pip install --upgrade package-name
echo.
echo Remove packages:
echo   conda remove package-name
echo   pip uninstall package-name
echo.
echo ENVIRONMENT INFORMATION:
echo ----------------------------------------------------------------
echo Current environment details:
echo   Name: AI2025
echo   Type: Conda environment
echo   Python version: 3.10.18
echo   Location: D:\AI_Environment\Miniconda\envs\AI2025
echo.
echo Check Python location:
echo   where python
echo.
echo Check pip location:
echo   where pip
echo.
echo TROUBLESHOOTING:
echo ----------------------------------------------------------------
echo.
echo Problem: Wrong Python version
echo Solution:
echo   1. Check environment: echo %%CONDA_DEFAULT_ENV%%
echo   2. Should show: AI2025
echo   3. If not: conda activate AI2025
echo.
echo Problem: Package not found
echo Solution:
echo   1. Check if in correct environment: conda list
echo   2. Install if missing: pip install package-name
echo   3. Try alternative: conda install package-name
echo.
echo Problem: Import errors
echo Solution:
echo   1. Verify package installed: pip show package-name
echo   2. Check Python path: python -c "import sys; print^(sys.path^)"
echo   3. Reinstall if needed: pip install --force-reinstall package-name
echo.
echo VALIDATION:
echo ----------------------------------------------------------------
echo Validate installation:
echo   validate.bat
echo.
echo Test core functionality:
echo   python -c "import sys; print^('Python OK:', sys.executable^)"
echo   python -c "import pandas, numpy, requests; print^('Core packages OK'^)"
echo   python -c "import langchain, streamlit; print^('AI packages OK'^)"
echo.
echo PORTABLE ENVIRONMENT NOTES:
echo ----------------------------------------------------------------
echo - Environment is fully portable on USB drive
echo - No registry modifications on host system
echo - All packages stored in D:\AI_Environment
echo - Works on any Windows 11 computer
echo - No internet required after initial setup
echo.
echo BEST PRACTICES:
echo ----------------------------------------------------------------
echo - Always work in AI2025 environment for AI projects
echo - Use pip for most package installations
echo - Use conda for system-level packages
echo - Keep environment clean - remove unused packages
echo - Regular validation with validate.bat
echo - Backup important projects separately
) > "D:\AI_Environment\help\6_environment_management.txt"

echo [8/9] Creating shutdown procedures help...
(
echo SHUTDOWN PROCEDURES
echo ================================================================
echo.
echo PROPER SHUTDOWN SEQUENCE:
echo ----------------------------------------------------------------
echo Follow these steps to cleanly shut down the AI Environment:
echo.
echo Step 1 - Stop Ollama Server:
echo   taskkill /IM ollama.exe /F
echo.
echo Step 2 - Close VS Code ^(if open^):
echo   Alt+F4 or File ^> Exit
echo.
echo Step 3 - Close Jupyter Lab ^(if running^):
echo   Ctrl+C in Jupyter terminal, then type 'y'
echo.
echo Step 4 - Stop any Python scripts:
echo   Ctrl+C in terminals running Python
echo.
echo Step 5 - Deactivate Conda environment:
echo   conda deactivate
echo.
echo Step 6 - Close terminal:
echo   exit
echo.
echo QUICK SHUTDOWN:
echo ----------------------------------------------------------------
echo For quick shutdown, simply close the terminal window.
echo Windows will automatically clean up most processes.
echo.
echo However, Ollama may continue running in background.
echo To stop it manually:
echo   taskkill /IM ollama.exe /F
echo.
echo GRACEFUL APPLICATION SHUTDOWN:
echo ----------------------------------------------------------------
echo.
echo Jupyter Lab:
echo   1. Save all notebooks ^(Ctrl+S^)
echo   2. Close browser tabs
echo   3. In terminal: Ctrl+C
echo   4. When prompted: type 'y' and press Enter
echo.
echo VS Code:
echo   1. Save all files ^(Ctrl+Shift+S^)
echo   2. Close VS Code ^(Alt+F4 or File ^> Exit^)
echo   3. VS Code will remember your workspace
echo.
echo Streamlit Apps:
echo   1. Close browser tab
echo   2. In terminal: Ctrl+C
echo.
echo Python Scripts:
echo   1. Let script complete naturally, or
echo   2. Interrupt with Ctrl+C
echo.
echo CHECKING FOR RUNNING PROCESSES:
echo ----------------------------------------------------------------
echo Check Ollama:
echo   tasklist ^| findstr ollama
echo.
echo Check Python processes:
echo   tasklist ^| findstr python
echo.
echo Check VS Code:
echo   tasklist ^| findstr Code
echo.
echo Kill specific process:
echo   taskkill /IM process-name.exe /F
echo.
echo SAFE USB REMOVAL:
echo ----------------------------------------------------------------
echo Before unplugging USB drive:
echo.
echo 1. Complete shutdown sequence above
echo 2. Close all file explorers pointing to D: drive
echo 3. Right-click USB drive in system tray
echo 4. Select "Eject" or "Safely Remove Hardware"
echo 5. Wait for "Safe to remove" message
echo 6. Unplug USB drive
echo.
echo WARNING SIGNS - DON'T REMOVE USB YET:
echo ----------------------------------------------------------------
echo - "Device is currently in use" message
echo - Ollama still running ^(tasklist ^| findstr ollama^)
echo - VS Code still open with files from D: drive
echo - Command prompt still in D:\AI_Environment directory
echo - File transfer operations in progress
echo.
echo RESTART PROCEDURES:
echo ----------------------------------------------------------------
echo After shutdown, to restart AI Environment:
echo.
echo 1. Ensure USB drive is connected as D:
echo 2. Navigate to D:\AI_Environment
echo 3. Run: activate_ai_env.bat
echo 4. Wait for initialization
echo 5. Continue working
) > "D:\AI_Environment\help\7_shutdown_procedures.txt"

echo [9/9] Creating useful tips help...
(
echo USEFUL TIPS AND TROUBLESHOOTING
echo ================================================================
echo.
echo GENERAL BEST PRACTICES:
echo ----------------------------------------------------------------
echo - Always work in the AI2025 environment for AI projects
echo - Use 'ollama list' to see what models you have
echo - Models are stored in: D:\AI_Environment\Models
echo - Your projects go in: D:\AI_Environment\Projects
echo - VS Code automatically uses the correct Python interpreter
echo - All AI libraries are pre-installed and ready to use
echo - Run 'validate.bat' if you encounter any issues
echo.
echo PERFORMANCE TIPS:
echo ----------------------------------------------------------------
echo - Use USB 3.0+ ports for better speed
echo - Close unnecessary applications to free up RAM
echo - Use SSD-based USB drives for optimal performance
echo - Keep models on the USB drive to avoid copying
echo - First model load takes longer - subsequent loads are faster
echo - Use smaller models ^(phi^) for quick testing
echo.
echo DEVELOPMENT WORKFLOW:
echo ----------------------------------------------------------------
echo 1. Start: activate_ai_env.bat
echo 2. Check models: ollama list
echo 3. Start development: code . or jupyter lab
echo 4. Test AI: ollama run llama2
echo 5. Build projects in: D:\AI_Environment\Projects
echo.
echo COMMON ISSUES AND SOLUTIONS:
echo ----------------------------------------------------------------
echo.
echo Problem: "Python not found"
echo Solution: Make sure you activated the environment with activate_ai_env.bat
echo.
echo Problem: "Ollama connection failed"
echo Solution: Start Ollama server with 'ollama serve' in separate terminal
echo.
echo Problem: "VS Code won't start"
echo Solution: Check if antivirus is blocking the executable
echo.
echo Problem: "Slow performance"
echo Solution: Use USB 3.0+ port and SSD-based USB drive
echo.
echo Problem: "Package import errors"
echo Solution: Run the validation tool to check installation
echo.
echo Problem: "Model not found"
echo Solution: Download with 'ollama pull model-name'
echo.
echo Problem: "Out of memory"
echo Solution: Close other applications, use smaller models
echo.
echo KEYBOARD SHORTCUTS:
echo ----------------------------------------------------------------
echo VS Code:
echo - Ctrl+Shift+P: Command palette
echo - F5: Run/Debug
echo - Ctrl+`: Open terminal
echo - Ctrl+Shift+E: Explorer
echo.
echo Ollama Chat:
echo - /bye: Exit chat
echo - Ctrl+C: Force exit
echo - Up arrow: Previous command
echo.
echo Jupyter:
echo - Shift+Enter: Run cell
echo - Ctrl+Enter: Run cell, stay in cell
echo - A: Insert cell above
echo - B: Insert cell below
echo.
echo PRODUCTIVITY TIPS:
echo ----------------------------------------------------------------
echo - Save frequently ^(Ctrl+S in VS Code^)
echo - Use Git for version control of projects
echo - Create templates for common AI tasks
echo - Keep a project log of what works
echo - Use descriptive filenames and comments
echo - Test with simple prompts first
echo.
echo MODEL SELECTION GUIDE:
echo ----------------------------------------------------------------
echo - phi:2.7b      - Fastest, good for testing
echo - mistral:7b    - Balanced speed and quality
echo - llama2:7b     - High quality, general purpose
echo - codellama:7b  - Best for programming tasks
echo.
echo Start with phi for development, switch to llama2 for production.
echo.
echo TROUBLESHOOTING CHECKLIST:
echo ----------------------------------------------------------------
echo When things go wrong:
echo 1. Is AI2025 environment active? ^(check prompt^)
echo 2. Is Ollama running? ^(tasklist ^| findstr ollama^)
echo 3. Is USB drive properly connected as D:?
echo 4. Any antivirus blocking executables?
echo 5. Sufficient RAM available? ^(check Task Manager^)
echo 6. All files in correct locations? ^(run validate.bat^)
echo.
echo GETTING HELP:
echo ----------------------------------------------------------------
echo - Run: validate.bat for system health check
echo - Check log files in: D:\AI_Environment\Logs\
echo - Review this help system: help\help_menu.bat
echo - Check official documentation for specific tools
echo - Test with minimal examples first
) > "D:\AI_Environment\help\8_useful_tips.txt"

echo.
echo ================================================================
echo               HELP SYSTEM SETUP COMPLETE!
echo ================================================================
echo.
echo Help system created successfully at: D:\AI_Environment\help\
echo.
echo Files created:
echo   [OK] help_menu.bat
echo   [OK] 1_ollama_models.txt
echo   [OK] 2_vscode_usage.txt
echo   [OK] 3_python_development.txt
echo   [OK] 4_project_examples.txt
echo   [OK] 5_manage_ollama.txt
echo   [OK] 6_environment_management.txt
echo   [OK] 7_shutdown_procedures.txt
echo   [OK] 8_useful_tips.txt
echo.
echo To use the help system:
echo   1. Navigate to: D:\AI_Environment
echo   2. Run: help\help_menu.bat
echo.
echo The help system is now ready to use!
echo.
pause
