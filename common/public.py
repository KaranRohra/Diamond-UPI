import smtplib
from random import randint
from email.message import EmailMessage


def send_mail(reciever_email, otp):
    msg = EmailMessage()
    msg.set_content(f"""
    Diamon UPI
    OTP: {otp}
    Don't Share with anyone
    We Don't call you and ask for OTP, Password and any other details
    """)

    msg['Subject'] = 'Diamon UPI OTP'
    msg['From'] = 'krohra138@gmail.com'
    msg['To'] = reciever_email

    # Send the message via our own SMTP server.
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login('krohra138@gmail.com', "karan138@")
        server.send_message(msg)
        server.quit()
    except:
        return False
    return True


def generate_otp():
    otp = randint(1,9)
    for i in range(5):
        otp = otp * 10 + randint(0,9)
    return otp