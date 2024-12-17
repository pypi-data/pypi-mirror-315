"""Terminal-based GUI for fsl-pipe."""
from .run import run_gui  # noqa F401
import importlib.metadata

__version__ = importlib.metadata.version("fsl_pipe_gui")
