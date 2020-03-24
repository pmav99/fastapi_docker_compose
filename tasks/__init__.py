import pathlib

from invoke import task

from .utils import chdir


TASKS_DIR = pathlib.Path(__file__).parent.expanduser().resolve()
REPO_DIR = TASKS_DIR.parent
WEB_DIR = REPO_DIR / "web"

@task
def export_requirements(c):
    with chdir(WEB_DIR):
        c.run(f"poetry export -f requirements.txt       -o {WEB_DIR.as_posix()}/requirements/requirements.txt")
        c.run(f"poetry export -f requirements.txt --dev -o {WEB_DIR.as_posix()}/requirements/requirements-dev.txt")
