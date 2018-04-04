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

    print('\nemail msg: {}\n'.format(msg))

    try:
        print('\nstart\n')
        server = smtplib.SMTP('smtp.gmail.com', 587)
        print('\nemail server created\n')
        server.starttls()
        print('\nemail server started\n')
        server.login('liquidemocracy.app@gmail.com', "NxTQj*hTBX7,%|@6")
        print('\nlogged into email server\n')
        server.sendmail('liquidemocracy.app@gmail.com', user_email, msg.as_string())
        print('\nsent email\n')
    except Exception as e:
        print("Email error:", e)
    finally:
        server.quit()
