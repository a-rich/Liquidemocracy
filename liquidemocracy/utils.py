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
        print('\nStart of send email...\n')
        server = smtplib.SMTP('smtp.gmail.com', 587)
        print('\nCreated email server\n')
        server.starttls()
        print('\nStarted email server\n')
        server.login('liquidemocracy.app@gmail.com', "NxTQj*hTBX7,%|@6")
        print('\nLogged into email\n')
        server.sendmail('liquidemocracy.app@gmail.com', user_email, msg.as_string())
        print('\nSent email\n')
    except Exception as e:
        print("Email error:", str(e))
    finally:
        server.quit()
