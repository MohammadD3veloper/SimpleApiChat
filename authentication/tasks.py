from re import sub
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_email(username:None, email:None, code: None, uid: None, token: None):
    subject = 'Email Activation'
    to_email = email
    username = username
    html_text = \
    f"""
    Hi {username}
    Thanks for sign up to our website!
    This email is for Activation your email address
    here is your code: {code}
    put this code in the following link form and 
    after that your account will be fully activation
    here is the link:
    <a href='http://127.0.0.1:8000/v1/api/auth/activate_email/{uid}/{token}/'>Click Me</a>
    So thanks for choosing us dear {username}!
    """
    send_mail(
        subject=subject,
        message='',
        html_message=html_text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[to_email]
    )
        

@shared_task
def send_any_email(subject, text, email):
    send_mail(subject=subject, message='', html_message=text, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[email])