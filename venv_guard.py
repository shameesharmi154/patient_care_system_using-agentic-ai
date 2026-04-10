"""Small helper to verify required packages are available and print helpful venv instructions.
Usage: at top of scripts call `venv_guard.ensure_requirements_exists(['flask'])`
"""
import os
import sys

def ensure_requirements_exist(modules):
    """Check each module in `modules` can be imported; if not, print helpful instructions and exit.

    This intentionally avoids auto re-exec because paths with spaces on Windows can fail.
    """
    missing = []
    for m in modules:
        try:
            __import__(m)
        except Exception:
            missing.append(m)

    if missing:
        venv_py = os.path.join(os.path.dirname(__file__), ".venv", "Scripts", "python.exe")
        print('\n✗ Missing Python packages:', ', '.join(missing))
        print('Please run the script using the project virtual environment Python and ensure dependencies are installed.')
        print('\nExamples:')
        print(f"  PowerShell: & \"{venv_py}\" script_name.py")
        print('  CMD: .venv\\Scripts\\activate.bat && python script_name.py')
        print('\nOr install dependencies into your current Python environment:')
        print('  python -m pip install -r requirements.txt')
        sys.exit(1)
