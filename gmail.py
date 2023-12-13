import os
from email.message import EmailMessage
import ssl
import smtplib

def send_email(day, train_price, plane_price):
    key = ''

    email_sender = ''
    email_password = key
    email_receiver = ''

    subject = 'Expensive trains lead to Climate Change!'
    body = """
    Dear Andy Slaughter,

    I am a student at Imperial College London, and I have been \
    tracking the price of trains and planes for this winter holiday season.

    I am shocked to tell you that traveling from London to Paris on December {}\
    by train (£{}) is more expensive than travelling there by plane (£{})!

    Legislation should not allow this as it makes consumers have to choose\
    between the environment and price. The climate emergency demands for \
    the cheaper options to be the environmentally friendly ones!

    I urge you to push for more train subsidies, and the end of plane subsidies.

    Thank you,
    Oriane Bui
    """
    body = body.format(day, train_price, plane_price)

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())