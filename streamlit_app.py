"""Streamlit Cloud entry point.

The app lives in a folder whose name contains spaces, which breaks Streamlit
Cloud's dependency install. Deploying this root-level file avoids that: it puts
the app folder on the import path and runs app.py from there.
"""
import runpy
import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent / "Agentic UAE Expansion Advisor"

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

runpy.run_path(str(APP_DIR / "app.py"), run_name="__main__")
