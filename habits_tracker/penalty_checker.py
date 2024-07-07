# habits_tracker/penalty_checker.py

from datetime import datetime
import json
from .config import LOG_FILE, PROMISOR, WARNING_TIME, PUNITION_TIME
from .email_service import EmailService


class PenaltyChecker:
    @staticmethod
    def check_late_submission_punition():
        now = datetime.now()
        existing_data = PenaltyChecker.load_existing_data(now.date())
        penalty_missed = 100
        if existing_data == {}:
            EmailService.send_email("Punition activée", f"{PROMISOR} a manqué la soumission avant {PUNITION_TIME}. Pénalité appliquée: {penalty_missed} CHF")
        else:
            EmailService.send_email("Bravo", "Bravo, tu as remplis ton obligation de lève tôt. Cours pour commencer le travail avant 10am!")

    @staticmethod
    def check_late_submission_warning():
        now = datetime.now()
        existing_data = PenaltyChecker.load_existing_data(now.date())
        if existing_data == {}:
            EmailService.send_email("Warning activée", f"{PROMISOR} a manqué la soumission avant {WARNING_TIME}. Il doit s'activer le vilain")
        else:
            EmailService.send_email("Bravo", "Bravo, tu as remplis ton obligation de lève tôt. Cours pour commencer le travail avant 10am!")

    @staticmethod
    def load_existing_data(log_date):
        try:
            with open(LOG_FILE, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        log_date_str = log_date.strftime("%Y-%m-%d")
        return data.get(log_date_str, {})
