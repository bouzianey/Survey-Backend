#flask mail
from flask_mail import Message
from flask_mail import Mail
from decorators import async_
from flask import render_template
from config import mail_settings
from init import app

app.config.update(mail_settings)
mail = Mail(app)


@async_
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(sender, recipient, student_name, student_email, pass_word):
    subject = 'Invitation to access your account'
    msg = Message(subject, sender=sender, recipients=recipient)
    msg.html = render_template('invitation.html', name=student_name, email=student_email, pwd=pass_word)
    send_async_email(app, msg)
