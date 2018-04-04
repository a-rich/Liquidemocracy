import smtplib
import email.utils
from email.mime.text import MIMEText

def send_email(user_email, subject, html):
    """
        Sends an account activation email to the user. Also used to send
        account recovery emails.
    """

    msg = MIMEText(html, 'html')
    msg['To'] = email.utils.formataddr(('Recipient', user_email))
    msg['From'] = email.utils.formataddr(('Liquidemocracy', 'liquidemocracy.app@gmail.com'))
    msg['Subject'] = subject

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('liquidemocracy.app@gmail.com', "NxTQj*hTBX7,%|@6")
        server.sendmail('liquidemocracy.app@gmail.com', user_email, msg.as_string())
        print('\nSent email\n')
    except Exception as e:
        return "Email error: " + e
    finally:
        server.quit()
