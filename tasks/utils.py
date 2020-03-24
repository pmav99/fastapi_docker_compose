import contextlib
import os
import pathlib


@contextlib.contextmanager
def chdir(dirname: str):
    curdir = os.getcwd()
    try:
        os.chdir(dirname)
        yield
    finally:
        os.chdir(curdir)
