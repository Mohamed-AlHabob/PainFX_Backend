# backend/booking_app/tasks.py

from celery import shared_task
from apps.booking_app.models import Notification, Payment
from django.core.mail import send_mail
from twilio.rest import Client
from django.conf import settings
from django.utils.timezone import now

# Twilio Configuration
TWILIO_ACCOUNT_SID = settings.TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN = settings.TWILIO_AUTH_TOKEN
TWILIO_FROM_NUMBER = settings.TWILIO_FROM_NUMBER

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
def process_payment_webhook(event_data):
    try:
        # Extract payment intent details
        payment_intent = event_data['data']['object']
        payment_id = payment_intent['id']
        status = payment_intent['status']

        # Fetch and update the Payment model
        payment = Payment.objects.get(payment_intent_id=payment_id)
        payment.payment_status = status
        payment.last_updated = now()
        payment.save()

        # Log success
        print(f"Payment {payment_id} processed successfully with status {status}")
    except Payment.DoesNotExist:
        print(f"Payment with intent ID {payment_id} not found.")
    except Exception as e:
        print(f"Error processing payment webhook: {str(e)}")

@shared_task
def send_email_notification(user_email, subject, message):
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )
