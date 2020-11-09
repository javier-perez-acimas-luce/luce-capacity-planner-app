import os
import yaml

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


def is_key_in_config_file(config_file, key):
    """
    Tests whether a yaml object contains a key
    :param conf: yaml object
    :param key: string key
    :param values: list of string values
    :return: true id all values contained in key, otherwise false
    """
    return key in config_file


def fetch_env_variable(config: str, var: str, group=None):
    """
    Tries to fecth a var from environment, otherwise uses the config_file one
    :param config_path: str path where the config file with YAML can be found.
    :param var: str var name.
    :param group: (optional) str var grouping name name.
    :return: var value
    """

    env_value = os.environ.get(var)

    if env_value is None:
        env_value = config[var] if group is None else config[group][var]

    return env_value


