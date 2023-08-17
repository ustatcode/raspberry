import smtplib
from email.message import EmailMessage
from gpiozero import Button


def send_email(subject, body, to_email):
    # Your email credentials
    email_address = 'sohampy0@gmail.com'
    email_password = 'ramacazhlhbkcipwxx'

    # Create the email message
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = email_address
    msg['To'] = to_email

    # Connect to Gmail's SMTP server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)


button = Button(2)
button.wait_for_press()
print('button pressed')
send_email('testing from raspberry with 2', 'some one is here, SOS',
           'email1@gmail.com,email2@gmail.com')
print('email sent')
