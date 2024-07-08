import os
from pydantic import BaseModel
from typing import Dict, List
import logging
import yaml
import json
from habits_tracker.utils import load_yaml_as_dict

# Initialize logging
logger = logging.getLogger(__name__)


class MailClientConfig(BaseModel):
    NOTIFICATION_EMAILS: List[str]
    EMAIL_SENDER: str
    EMAIL_PASSWORD: str
    SMTP_SERVER: str
    SMTP_PORT: int

    @classmethod
    def from_env(cls):
        notification_emails = os.environ.get("NOTIFICATION_EMAILS").split(',')
        email_sender = os.environ.get("EMAIL_SENDER")
        email_password = os.environ.get("EMAIL_PASSWORD")
        smtp_server = os.environ.get("SMTP_SERVER")
        smtp_port = int(os.environ.get("SMTP_PORT"))

        if not all([notification_emails, email_sender, email_password, smtp_server, smtp_port]):
            raise ValueError("Please set all required email environment variables.")

        logger.info("Loaded MailClientConfig from environment variables.")
        return cls(
            NOTIFICATION_EMAILS=notification_emails,
            EMAIL_SENDER=email_sender,
            EMAIL_PASSWORD=email_password,
            SMTP_SERVER=smtp_server,
            SMTP_PORT=smtp_port
        )

    @classmethod
    def from_yaml(cls, yaml_path: str):
        if not os.path.exists(yaml_path):
            raise ValueError(f"{yaml_path} does not exist.")

        config_dict = load_yaml_as_dict(yaml_path)

        logger.info(f"Loaded MailClientConfig from {yaml_path}.")
        return cls(
            NOTIFICATION_EMAILS=config_dict.get('notification_emails'),
            EMAIL_SENDER=config_dict.get('email_sender'),
            EMAIL_PASSWORD=config_dict.get('email_password'),
            SMTP_SERVER=config_dict.get('smtp_server'),
            SMTP_PORT=config_dict.get('smtp_port')
        )


class HabitTrackerConfig(BaseModel):
    HABITS: Dict[str, str]
    LOG_FILE: str
    PENALTY_AMOUNT: int
    PROMISOR: str
    TOTAL_POOL: int    # CHF per month
    WARNING_TIME: str
    PUNITION_TIME: str

    @classmethod
    def from_env(cls):
        habits = os.environ.get("HABITS")
        log_file = os.environ.get("LOG_FILE")
        penalty_amount = int(os.environ.get("PENALTY_AMOUNT"))
        promisor = os.environ.get("PROMISOR")
        total_pool = int(os.environ.get("TOTAL_POOL"))
        warning_time = os.environ.get("WARNING_TIME")
        punition_time = os.environ.get("PUNITION_TIME")

        if not all([habits, log_file, penalty_amount, promisor, total_pool, warning_time, punition_time]):
            raise ValueError("Please set all required environment variables.")

        habits_dict = json.loads(habits)

        logger.info("Loaded HabitTrackerConfig from environment variables.")
        return cls(
            HABITS=habits_dict,
            LOG_FILE=log_file,
            PENALTY_AMOUNT=penalty_amount,
            PROMISOR=promisor,
            TOTAL_POOL=total_pool,
            WARNING_TIME=warning_time,
            PUNITION_TIME=punition_time
        )

    @classmethod
    def from_yaml(cls, yaml_path: str):
        if not os.path.exists(yaml_path):
            raise ValueError(f"{yaml_path} does not exist.")

        config_dict = load_yaml_as_dict(yaml_path)

        logger.info(f"Loaded HabitTrackerConfig from {yaml_path}.")
        return cls(
            HABITS=config_dict.get('habits'),
            LOG_FILE=config_dict.get('log_file'),
            PENALTY_AMOUNT=config_dict.get('penalty_amount'),
            PROMISOR=config_dict.get('promisor'),
            TOTAL_POOL=config_dict.get('total_pool'),
            WARNING_TIME=config_dict.get('warning_time'),
            PUNITION_TIME=config_dict.get('punition_time')
        )


class APIKeysConfig(BaseModel):
    OPENAI_KEY: str

    @classmethod
    def from_env(cls):
        openai_api_key = os.environ.get("OPENAI_API_KEY")

        if openai_api_key is None:
            raise ValueError("Please set OPENAI_API_KEY environment variable.")

        openai_api_key = openai_api_key.replace("'", "").replace('"', "")

        logger.info("Loaded API keys from environment variables.")
        return cls(OPENAI_KEY=openai_api_key)

    @classmethod
    def from_yaml(cls, yaml_path: str):
        if not os.path.exists(yaml_path):
            raise ValueError(f"{yaml_path} does not exist.")

        config_dict = load_yaml_as_dict(yaml_path)

        logger.info(f"Loaded API keys from {yaml_path}.")
        return cls(**config_dict)
