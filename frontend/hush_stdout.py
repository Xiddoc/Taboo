"""
Modules, stop printing to console...

https://stackoverflow.com/a/25061573/11985743
"""
from contextlib import contextmanager
from os import devnull
import sys


@contextmanager
def suppress_stdout():
    """
    Context manager to temporarily suppress STDOUT.
    """
    with open(devnull, "w") as dev:
        old_stdout = sys.stdout
        sys.stdout = dev
        try:
            yield
        finally:
            sys.stdout = old_stdout
