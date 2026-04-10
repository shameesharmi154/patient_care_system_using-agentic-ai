"""Wrapper to run Flask and capture all output"""
import sys
import os
import logging

# Guard: ensure Flask is available in the current interpreter before importing the app
try:
    import flask  # quick availability check
except Exception:
    venv_py = os.path.join(os.path.dirname(__file__), ".venv", "Scripts", "python.exe")
    print("\n✗ Flask is not available in this Python interpreter (ModuleNotFoundError).\n")
    print("Please run the script using the project's virtual environment Python, for example:\n")
    print(f"  PowerShell: $env:GEMINI_API_KEY='<YOUR_KEY>'; & \"{venv_py}\" run_flask.py")
    print(f"  CMD: .venv\\Scripts\\activate.bat && python run_flask.py\n")

    # If a venv python exists in the project, attempt to re-exec with it
    if os.path.exists(venv_py) and os.path.abspath(venv_py) != os.path.abspath(sys.executable):
        print("Attempting to run with the project's venv Python now...")
        os.execv(venv_py, [venv_py] + sys.argv)

    sys.exit(1)

# Now it's safe to import the app (Flask is available)
from app import app

# Set up logging to be very verbose
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(name)s: %(message)s')

if __name__ == "__main__":
    print("=" * 60)
    print("Starting Flask app with error capture...")
    print("=" * 60)
    try:
        app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
    except KeyboardInterrupt:
        print("\nShutdown requested")
    except Exception as e:
        print(f"\n✗ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
