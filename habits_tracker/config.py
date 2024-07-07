import os
import yaml
from typing import List
import logger

# habits_tracker/config.py
PENALTY_AMOUNT = 50  # CHF par engagement non tenu
TOTAL_POOL = 1000  # CHF par mois
# Remplacez par les emails des parties prenantes


SMTP_SERVER = 'smtp.mail.me.com'
SMTP_PORT = 587



LOG_FILE = "habits_log.json"

WARNING_TIME = "07:00"
PUNITION_TIME = "07:30"


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


class MailClientConfig:
    notification_emails: List[str]
    email_sender: str
    email_password: str

    @classmethod
    def from_env(cls):
        notification_emails = os.environ.get("NOTIFICATION_EMAILS")
        email_sender = os.environ.get("EMAIL_SENDER")
        email_password = os.environ.get("EMAIL_PASSWORD")

        if notification_emails is None:
            raise ValueError("Please set NOTIFICATION_EMAILS environment variables.")
        if email_sender is None:
            raise ValueError("Please set EMAIL_SENDER environment variables.")
        if email_password is None:
            raise ValueError("Please set EMAIL_PASSWORD environment variables.")

        logger.info("Loaded notification_emails, email_sender, email_password from environment variables.")
        logger.info(f"NOTIFICATION_EMAILS: {notification_emails}")
        logger.info(f"EMAIL_SENDER: {email_sender}")
        logger.info(f"EMAIL_PASSWORD: {email_password}")

        return cls(notification_emails=notification_emails, email_sender=email_sender, email_password=email_password)

    @classmethod
    def from_yaml(cls, yaml_path: str):
        if not os.path.exists(yaml_path):
            raise ValueError(f"{yaml_path} does not exist.")

        config_dict = load_yaml_as_dict(yaml_path)

        logger.info(f"Loaded notification_emails, email_sender, email_password from {yaml_path}.")
        logger.info(f"NOTIFICATION_EMAILS: {config_dict['notification_emails']}")
        logger.info(f"EMAIL_SENDER: {config_dict['email_sender']}")
        logger.info(f"EMAIL_PASSWORD: {config_dict['email_password']}")

        return cls(**config_dict)


# OPENAI Configs
class APIKeysConfig(BaseModel):
    openai: str

    @classmethod
    def from_env(cls):
        openai_api_key = os.environ.get("OPENAI_API_KEY")

        if openai_api_key is None:
            raise ValueError("Please set OPENAI_API_KEY environment variables.")

        # remove ' and " from the keys
        openai_api_key = openai_api_key.replace("'", "").replace('"', "")

        if openai_api_key is None:
            raise ValueError("Please set OPENAI_API_KEY environment variables.")

        logger.info("Loaded API keys from environment variables.")
        logger.info(f"OPENAI_API_KEY: {openai_api_key}")

        return cls(openai=openai_api_key)

    @classmethod
    def from_yaml(cls, yaml_path: str):
        if not os.path.exists(yaml_path):
            raise ValueError(f"{yaml_path} does not exist.")

        config_dict = load_yaml_as_dict(yaml_path)

        logger.info(f"Loaded API keys from {yaml_path}.")
        logger.info(f"OPENAI_API_KEY: {config_dict['openai']}")

        return cls(**config_dict)