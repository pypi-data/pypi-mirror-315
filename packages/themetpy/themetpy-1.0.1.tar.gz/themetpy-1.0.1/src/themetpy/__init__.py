import logging
from importlib.metadata import version

# Define the version of the package
__version__ = version("themetpy")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import only necessary top-level objects
from .departments import get_departments
from .objects import get_object, get_all_object_ids
from .search import search
from .utils import handle_missing_data

# Define public API of the package
__all__ = [
    "get_departments",
    "get_all_object_ids",
    "get_object",
    "search",
    "handle_missing_data",
]