from django.conf import settings
import smtplib
from email.mime.text import MIMEText


def send_email(email, theme, message):
    try:
        msg = MIMEText(message)
        msg['Subject'] = theme
        msg['From'] = settings.SITE_EMAIL
        msg['To'] = email
        s = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
        s.connect(settings.SMTP_SERVER, settings.SMTP_PORT)
        s.starttls()
        s.ehlo()
        s.login(settings.SITE_EMAIL, settings.EMAIL_PASSWORD)
        s.sendmail(settings.SITE_EMAIL, [email], msg.as_string())
        s.quit()
    except Exception as e:
        settings.LOG.err("libs.send_email. {}".format(e))
