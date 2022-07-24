# *******************************************************************************************
#  File:  support.py
#
#  Created: 24-07-2022
#
#  History:
#  24-07-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__contact__ = "james@developernotes.org"
__copyright__ = "Copyright (c) 2022 James Dooley <james@dooley.ch>"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"

__all__ = ['find_folder']

from pathlib import Path


def find_folder(name: str, root: Path | str | None = None) -> Path | None:
    """
    This function finds and returns the location of the folder with the given name
    :param name: The name of the folder to search for
    :param root: The folder where to begin the search
    """
    if root is None:
        root = Path(__file__).parent

    if isinstance(root, str):
        root = Path(root)

    # Check current folder
    if name == root.name:
        return root

    # Search current folder
    results = root.glob(name)
    for folder in results:
        if folder.name == name:
            return root.joinpath(folder)

    # Move up a folder
    parent_folder = root.parent
    if not parent_folder.name:
        return None

    return find_folder(name, parent_folder)
