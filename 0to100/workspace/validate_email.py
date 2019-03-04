import os
from threading import Thread

import sendgrid
from sendgrid.helpers.mail import Email as SGEmail, Content, Mail as SGMail
from flask_mail import Mail, Message
from flask import Flask, flash, redirect, url_for, render_template, request, current_app


current_app.jinja_env.trim_blocks = True
current_app.jinja_env.lstrip_blocks = True

current_app.config.update(
    SECRET_KEY=os.getenv('SECRET_KEY', 'secret string'),
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER=('Grey Li', os.getenv('MAIL_USERNAME'))
)

mail = Mail(current_app)


def send_smtp_mail(subject, to, body):
    message = Message(subject, recipients=[to], body=body)
    mail.send(message)

@app.route('/login', methods=['GET', 'POST'])
def index():
    to = '123hosumlai@gmail.com'
    subject = "just a test"
    body = "I just said its a test"
    if request.method == 'POST':
        send_smtp_mail(subject, to, body)
        
        return redirect(url_for('index'))

    return render_template('index.html', form=form)