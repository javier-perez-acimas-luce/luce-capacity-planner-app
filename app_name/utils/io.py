"""
    Utils for IO on datalake files

    File name: io.py
    Author: Teresa Paramo
    Date created: 09/02/2021
    Date last modified: 09/02/2021
    Python Version: 3.8
"""

import os
import time

import yaml


def get_date_sub_path(file_name):
    """
    Generates a subpath from a date, according to the structure: year/month/day/file_name
    :file_name date: string file name
    :return: string subpath corresponding to the input path.
    """
    return time.strftime("%Y") + "/" + time.strftime("%m") + "/" + time.strftime("%d") + "/" + file_name


def load_config(config_file: str):
    """
    Loads a Python config file with YAML.
    :param config_file: str path where the config file with YAML can be found.
    :return: yaml file
    """
    with open(config_file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise exc


def is_key_in_config_file(config_file, key, values):
    """
    Tests whether a yaml object contains certain keys and values associated
    :param config_file: yaml object
    :param key: string key
    :param values: list of string values
    :return: true id all values contained in key, otherwise false
    """
    result = False
    is_key = key in config_file
    if is_key:
        subkeys = config_file[key].keys()
        result = all([(x in subkeys and config_file[key][x] != "") for x in values])
    return result


def is_key_in_config_file(config_file, key):
    """
    Tests whether a yaml object contains a key
    :param config_file: yaml object
    :param key: string key
    :return: true id all values contained in key, otherwise false
    """
    return key in config_file


def fetch_env_variable(config: str, var: str, group=None):
    """
    Tries to fetch a var from environment, otherwise uses the config_file one
    :param config: str path where the config file with YAML can be found.
    :param var: str var name.
    :param group: (optional) str var grouping name name.
    :return: var value
    """

    env_value = os.environ.get(var)

    if env_value is None:
        env_value = config[var] if group is None else config[group][var]

    return env_value
