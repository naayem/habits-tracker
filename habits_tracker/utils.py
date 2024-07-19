import os
import yaml


def load_yaml_as_dict(config_path: str) -> dict:
    """Load a configuration file from a given path.

    Args:
        config_path (str): Path to the configuration file.

    Returns:
        dict: Configuration file as a dictionary.
    """
    with open(config_path) as f:
        config_dict = yaml.safe_load(f)
    return config_dict


def load_env_from_yaml(yaml_path):
    try:
        with open(yaml_path, 'r') as f:
            config = yaml.safe_load(f)
            for key, value in config.items():
                os.environ[key] = str(value)
    except FileNotFoundError as fnf_error:
        print(fnf_error)

# Example usage
# load_env_from_yaml(".secrets.yaml")
