from email.mime.multipart import MIMEMultipart
import smtplib
from email.mime.text import MIMEText
from .config import MailClientConfig
import logging

# Initialize logging
logger = logging.getLogger(__name__)


class EmailService:
    def send_email(subject, body, config: MailClientConfig):
        for receiver in config.NOTIFICATION_EMAILS:
            msg = MIMEMultipart()
            msg.attach(MIMEText(body, "plain"))
            msg['Subject'] = subject
            msg['From'] = config.EMAIL_SENDER
            msg['To'] = receiver

            try:
                with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT) as server:
                    server.starttls()
                    server.login(config.EMAIL_SENDER, config.EMAIL_PASSWORD)
                    server.sendmail(config.EMAIL_SENDER, receiver, msg.as_string())
                    logger.info(f"Email sent to {receiver}")
            except smtplib.SMTPException as e:
                logger.error(f"Failed to send email to {receiver}: {e}")
            except Exception as e:
                logger.error(f"An error occurred: {e}")

    def send_email_promisor(subject, body, config: MailClientConfig):
        PROMISOR_EMAIL = config.NOTIFICATION_EMAILS[0]
        msg = MIMEMultipart()
        msg.attach(MIMEText(body, "plain"))
        msg['Subject'] = subject
        msg['From'] = config.EMAIL_SENDER
        msg['To'] = PROMISOR_EMAIL

        try:
            with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT) as server:
                server.starttls()
                server.login(config.EMAIL_SENDER, config.EMAIL_PASSWORD)
                server.sendmail(config.EMAIL_SENDER, PROMISOR_EMAIL, msg.as_string())
                logger.info(f"Email sent to {PROMISOR_EMAIL}")
        except smtplib.SMTPException as e:
            logger.error(f"Failed to send email to {PROMISOR_EMAIL}: {e}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
