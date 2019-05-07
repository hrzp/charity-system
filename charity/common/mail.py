from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from charity.serverbase import ErrorToClient
import os


def send_mail(to, subject, html):
    message = Mail(
        from_email='charitySystem@lsbits.com',
        to_emails=to,
        subject=subject,
        html_content=html)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
        raise ErrorToClient('Error on sending mail')
