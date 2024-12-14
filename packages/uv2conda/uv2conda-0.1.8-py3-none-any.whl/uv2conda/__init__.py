import importlib.metadata

from .conda import make_conda_env_from_dependencies
from .conda import make_conda_env_from_project_dir
from .conda import make_conda_env_from_requirements_file
from .pip import read_requirements_file
from .uv import get_requirents_from_project_dir
from .uv import write_requirements_file_from_project_dir

__all__ = [
    "get_requirents_from_project_dir",
    "make_conda_env_from_dependencies",
    "make_conda_env_from_project_dir",
    "make_conda_env_from_requirements_file",
    "read_requirements_file",
    "write_requirements_file_from_project_dir",
]

__version__ = importlib.metadata.version(__name__)
