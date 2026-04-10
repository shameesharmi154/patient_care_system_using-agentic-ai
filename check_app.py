import os
import sys

# Guard: ensure Flask is available in the current interpreter before importing the app
try:
    import flask  # quick availability check
except Exception:
    venv_py = os.path.join(os.path.dirname(__file__), ".venv", "Scripts", "python.exe")
    print("\n✗ Flask is not available in this Python interpreter (ModuleNotFoundError).\n")
    print("Please run the script using the project's virtual environment Python, for example:\n")
    print(f"  PowerShell: & \"{venv_py}\" check_app.py")
    print(f"  CMD: .venv\\Scripts\\activate.bat && python check_app.py\n")

    # If a venv python exists, we will NOT auto-reexec on Windows because
    # paths with spaces can cause the launch to fail. Instead, print exact
    # commands the user should run and exit with a helpful message.
    print("Please run the script using the project's venv Python as shown above and re-run the command.")
    sys.exit(1)

from app import app
import routes

with app.test_client() as c:
    r = c.get('/')
    print('STATUS', r.status_code)
    data = r.get_data(as_text=True)
    print('\n--- BODY (first 800 chars) ---\n')
    print(data[:800])