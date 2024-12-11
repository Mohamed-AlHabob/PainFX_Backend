from django.contrib import admin
from apps.booking_app.models import (
    Clinic,
    ClinicDoctor,
    Reservation,
    Review, Post,
    Comment, Like, Category, Subscription, PaymentMethod,
    Payment, Notification, EventSchedule, AdvertisingCampaign,
    UsersAudit
)
admin.site.register(Clinic)
admin.site.register(ClinicDoctor)
admin.site.register(Reservation)
admin.site.register(Review) 
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Category)
admin.site.register(Subscription)
admin.site.register(PaymentMethod)
admin.site.register(Payment)
admin.site.register(Notification)
admin.site.register(EventSchedule)
admin.site.register(AdvertisingCampaign)
admin.site.register(UsersAudit)

