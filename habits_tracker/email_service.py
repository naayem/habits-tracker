from email.mime.multipart import MIMEMultipart
import smtplib
from email.mime.text import MIMEText
from .config import EMAIL_SENDER, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT, NOTIFICATION_EMAILS


class EmailService:
    @staticmethod
    def send_email(subject, body):
        for receiver in NOTIFICATION_EMAILS:
            msg = MIMEMultipart()
            msg.attach(MIMEText(body, "plain"))
            msg['Subject'] = subject
            msg['From'] = EMAIL_SENDER
            msg['To'] = receiver

            try:
                with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                    server.starttls()
                    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
                    server.sendmail(EMAIL_SENDER, receiver, msg.as_string())
                    print(f"Email sent to {receiver}")
            except smtplib.SMTPException as e:
                print(f"Failed to send email to {receiver}: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")

    @staticmethod
    def send_email_promisor(subject, body):
        promisor_email = NOTIFICATION_EMAILS[0]
        msg = MIMEMultipart()
        msg.attach(MIMEText(body, "plain"))
        msg['Subject'] = subject
        msg['From'] = EMAIL_SENDER
        msg['To'] = promisor_email

        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(EMAIL_SENDER, EMAIL_PASSWORD)
                server.sendmail(EMAIL_SENDER, promisor_email, msg.as_string())
                print(f"Email sent to {promisor_email}")
        except smtplib.SMTPException as e:
            print(f"Failed to send email to {promisor_email}: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
