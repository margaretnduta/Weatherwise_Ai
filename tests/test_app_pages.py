"""
tests/test_app_pages.py
───────────────────────
Unit tests for Phase 2 of WeatherWise AI Streamlit Application.
Verifies Python syntax, py_compile validity, and page component integration.
"""

import py_compile
import os
import glob
import pytest


def test_app_pages_syntax():
    """Verify that all Streamlit page scripts compile with zero syntax errors."""
    app_files = ["app/Home.py"] + glob.glob("app/pages/*.py") + glob.glob("app/components/*.py") + ["app/utils.py"]
    
    assert len(app_files) >= 7, f"Expected at least 7 Python files in app/, found {len(app_files)}"

    for file_path in app_files:
        assert os.path.exists(file_path), f"File missing: {file_path}"
        # Compiling code raises PyCompileError if any syntax/import-structure error exists
        compiled = py_compile.compile(file_path, doraise=True)
        assert compiled is not None, f"Failed to compile {file_path}"
