from datetime import datetime
import json

from habits_tracker.config import HabitTrackerConfig, MailClientConfig
from .email_service import EmailService


class PenaltyChecker:
    @staticmethod
    def check_late_submission_punition(habit_config: HabitTrackerConfig, mail_config: MailClientConfig):
        now = datetime.now()
        existing_data = PenaltyChecker.load_existing_data(now.date(), habit_config.LOG_FILE)
        penalty_missed = 100
        if existing_data == {}:
            EmailService.send_email("Punition activée", f"{habit_config.PROMISOR} a manqué la soumission avant {habit_config.PUNITION_TIME}. Pénalité appliquée: {penalty_missed} CHF", mail_config)
        else:
            EmailService.send_email("Bravo", "Bravo, tu as remplis ton obligation de lève tôt. Cours pour commencer le travail avant 10am!", mail_config)

    @staticmethod
    def check_late_submission_warning(habit_config: HabitTrackerConfig, mail_config: MailClientConfig):
        now = datetime.now()
        existing_data = PenaltyChecker.load_existing_data(now.date(), habit_config.LOG_FILE)
        if existing_data == {}:
            EmailService.send_email("Warning activée", f"{habit_config.PROMISOR} a manqué la soumission avant {habit_config.WARNING_TIME}. Il doit s'activer le vilain", mail_config)
        else:
            EmailService.send_email("Bravo", "Bravo, tu as remplis ton obligation de lève tôt. Cours pour commencer le travail avant 10am!", mail_config)

    @staticmethod
    def load_existing_data(log_date, LOG_FILE):
        try:
            with open(LOG_FILE, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        log_date_str = log_date.strftime("%Y-%m-%d")
        return data.get(log_date_str, {})
