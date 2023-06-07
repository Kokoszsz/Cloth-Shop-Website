
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def generate_verification_code():
    code = random.randint(100000, 999999)
    return str(code)


def account_registration_verification(message, verification_code):
    text = f"""\
        Hi,
        Check you verificaiton code
        {verification_code}
        """
    
    part1 = MIMEText(text, "plain")

    message.attach(part1)

    return message


def send_email(type_of_message, receiver):

    sender = 'email adress that sends message'
    sender_password = 'password to that email'

    server = smtplib.SMTP('smtp-mail.outlook.com', 587)
    server.starttls()
    server.login(sender, sender_password)

    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender
    message["To"] = receiver


    if type_of_message == 'account registration verification':
        verification_code = generate_verification_code()
        message = account_registration_verification(message, verification_code)
    else:
        # email has not been sent
        return None
    

    server.sendmail(message["From"], message["To"], message.as_string())
    server.quit()

    return verification_code
