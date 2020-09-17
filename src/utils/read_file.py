"""
    Utils for IO on datalake files

    File name: test_read_utils.py
    Author: Teresa Paramo
    Date created: 7/22/2018
    Date last modified: 7/22/2018
    Python Version: 3.6
"""


import yaml


def get_date_sub_path(date):
    """
    Generates a subpath from a date, according to the structure: year/yearmonth/yearmonthday
    :param date: datetime.date used for the subpath generation.
    :return: string subpath corresponding to the input date.
    """
    year = int(date.year)
    month = int(date.month)
    day = int(date.day)
    return '%04d/%04d%02d/%04d%02d%02d/' % (year, year, month, year, month, day)


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
    :param conf: yaml object
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


