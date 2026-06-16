from celery import shared_task
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_email(email, code):
    """ send link for activate user """
    if email and code:
        try:
            send_mail('active_account', f"{code}",
                      settings.EMAIL_HOST_USER, [email])
            print('Email sent successfully')
        except Exception as e:
            print(f'Error sending email: {e}')
    else:
        print('All fields are required')
