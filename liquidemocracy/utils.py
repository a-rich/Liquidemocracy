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
        print('Start of send email...')
        server = smtplib.SMTP('smtp.gmail.com', 587)
        print('Created email server')
        server.starttls()
        print('Started email server')
        #server.login('liquidemocracy.app@gmail.com', "NxTQj*hTBX7,%|@6")
        server.login('liquidemocracy.app@gmail.com', "uxiyufcpgjgqwhca")
        print('Logged into email')
        server.sendmail('liquidemocracy.app@gmail.com', user_email, msg.as_string())
        print('Sent email')
    except Exception as e:
        print("Email error:", str(e))
    finally:
        server.quit()
