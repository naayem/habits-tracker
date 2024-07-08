from habits_tracker.config import MailClientConfig, HabitTrackerConfig
from habits_tracker.utils import load_env_from_yaml
from habits_tracker.penalty_checker import PenaltyChecker
import logging

logging.basicConfig(filename='/var/log/cron.log', level=logging.INFO)


def main():
    logging.info('PUNITION')
    # Load environment variables from YAML
    load_env_from_yaml("/habits_tracker/.secrets.yaml")

    # Load configurations
    habit_tracker_config = HabitTrackerConfig.from_env()
    mail_client_config = MailClientConfig.from_env()

    PenaltyChecker.check_late_submission_punition(habit_tracker_config, mail_client_config)
    # Your script logic here


if __name__ == "__main__":
    main()
