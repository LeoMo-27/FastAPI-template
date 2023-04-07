"""
Used to set environment variable before running tests.
We need this to use test database.
"""

import os

# This will ensure using test database
os.environ["ENVIRONMENT"] = "PYTEST"
