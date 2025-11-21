# -*- coding: utf-8 -*-
"""
Perform file management operations for the SYMORO package.
"""

from pathlib import Path

SYMORO_ROBOTS_FOLDER = "symoro-robots"


def get_base_path(base_folder: str = SYMORO_ROBOTS_FOLDER) -> Path:
    """
    Return the base path for storing all SYMORO robot files.

    Returns:
        Path object specifying the base folder path.
    """
    home_folder = Path.home()
    return home_folder / base_folder


def get_clean_name(name: str, char: str = '-') -> str:
    """
    Return a cleaned lowercase version of a name, replacing spaces with a specified character.
    """
    return name.strip().lower().replace(' ', char)


def make_folders(folder_path: Path) -> None:
    """
    Ensure a folder path exists (create it if necessary).
    """
    Path(folder_path).mkdir(parents=True, exist_ok=True)


def get_folder_path(robot_name: str) -> Path:
    """
    Return and ensure the folder path for the given robot name.
    """
    robot_name = get_clean_name(robot_name)
    folder_path = get_base_path() / robot_name
    make_folders(folder_path)
    return folder_path


def get_file_path(robo, ext: str = None) -> Path:
    """
    Return the file path for a robot with the specified extension.

    Args:
        robo: An instance of the Robot class with attributes 'name' and 'directory'.
        ext: Optional extension string.
    """
    if ext is None:
        fname = f"{get_clean_name(robo.name)}.par"
    else:
        fname = f"{get_clean_name(robo.name)}_{ext}.txt"

    file_path = Path(robo.directory) / fname
    make_folders(file_path.parent)
    return file_path
