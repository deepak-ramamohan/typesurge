import sys
import os
from unittest.mock import patch, MagicMock

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- Global Mocks ---
# Use pytest_configure to apply patches at the start of the test session.

def pytest_configure(config):
    """
    Apply global mocks before any tests are collected.
    """
    # Patch the specific functions that are causing issues
    # during test collection.
    patch('arcade.Sound', MagicMock()).start()
    patch('arcade.load_texture', MagicMock()).start()

def pytest_unconfigure(config):
    """
    Clean up the patches after the test session.
    """
    patch.stopall()
