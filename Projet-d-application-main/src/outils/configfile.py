# -*- coding: utf-8 -*-

"""
Setup, read, write a config file, folder for SYMORO package.
"""

import os
import configparser

CONFIG_FILE_NAME = 'settings.conf'


def get_prog_config_path():
    """
    Return the folder path for storing SYMORO program settings.

    Returns:
         A string specifying the path to store SYMORO settings.
    """
    prog_name = 'symoro'
    if os.name == 'nt':
        return os.path.join(os.environ['APPDATA'], prog_name)
    else:
        return os.path.join(os.environ['HOME'], '.config', prog_name)


def get_config_file_path():
    """
    Return the path for SYMORO settings file.

    Returns:
        A string specifying the path to SYMORO `settings.conf` file.
    """
    return os.path.join(get_prog_config_path(), CONFIG_FILE_NAME)


def make_config_folder():
    """
    Check if the config folder exists and create it if it does not exist.
    """
    config_folder_path = get_prog_config_path()
    if not os.path.exists(config_folder_path):
        os.makedirs(config_folder_path)


def save_config(curr_config):
    """
    Save the current configuration to the disk in a file.

    Args:
        curr_config: An instance of the `configparser.ConfigParser` class.
    """
    make_config_folder()
    if not isinstance(curr_config, configparser.ConfigParser):
        raise TypeError(
            "`curr_config` should be an instance of `configparser.ConfigParser`"
        )
    config_file_path = get_config_file_path()
    with open(config_file_path, 'w', encoding='utf-8') as config_file:
        curr_config.write(config_file)


def get_config():
    """
    Return the program settings from the settings file. When a settings
    file does not exist, return a new settings object.

    Returns:
        A `configparser.ConfigParser` object with the program settings.
    """
    config = configparser.ConfigParser()
    config_file_path = get_config_file_path()
    if os.path.exists(config_file_path):
        config.read(config_file_path, encoding='utf-8')
    return config


def get_last_robot():
    """
    Return the path to the last used robot's PAR file.

    Returns:
        A string specifying the path to the last used robot's PAR file.
    """
    config = get_config()
    if config.has_option('startup', 'last-robot'):
        return config.get('startup', 'last-robot')
    return None


def set_last_robot(robo_par_file):
    """
    Set the last used robot in the settings file.

    Args:
        robo_par_file: A string specifying the path to robot's PAR file.
    """
    config = configparser.ConfigParser()
    config.add_section('startup')
    config.set('startup', 'last-robot', robo_par_file)
    save_config(config)
