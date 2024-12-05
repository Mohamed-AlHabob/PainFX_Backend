# backend/booking_app/tasks.py

from celery import shared_task
from apps.booking_app.models import Notification, Payment
from django.core.mail import send_mail
from twilio.rest import Client
from django.conf import settings

# Twilio Configuration
TWILIO_ACCOUNT_SID = 'your_twilio_account_sid'
TWILIO_AUTH_TOKEN = 'your_twilio_auth_token'
TWILIO_FROM_NUMBER = 'your_twilio_number'

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@shared_task
def send_sms_notification(user_id, message):
    from .models import User
    try:
        user = User.objects.get(id=user_id)
        # Assume User model has a phone_number field
        phone_number = user.profile.phone_number  # Adjust as per your UserProfile
        twilio_client.messages.create(
            body=message,
            from_=TWILIO_FROM_NUMBER,
            to=phone_number
        )
    except User.DoesNotExist:
        pass

@shared_task
def process_payment_webhook(payment_intent):
    # Implement your logic to handle payment events
    # For example, update Payment model status
    payment_id = payment_intent.get('id')
    status = payment_intent.get('status')
    # Fetch and update Payment model accordingly
    # This is a simplified example
    try:
        payment = Payment.objects.get(payment_intent_id=payment_id)
        payment.payment_status = status
        payment.save()
    except Payment.DoesNotExist:
        pass

@shared_task
def send_email_notification(user_email, subject, message):
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )
