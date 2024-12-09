# backend/booking_app/urls.py

from django.urls import path, include
from rest_framework import routers

from apps.booking_app.views import (
    CreateStripePaymentIntentView, PatientViewSet, DoctorViewSet,
    ClinicViewSet, ReservationViewSet, ReviewViewSet, PostViewSet,
    VideoViewSet, CommentViewSet, LikeViewSet, CategoryViewSet,
    SubscriptionViewSet, PaymentMethodViewSet, PaymentViewSet,
    NotificationViewSet, EventScheduleViewSet, AdvertisingCampaignViewSet,
    UsersAuditViewSet, stripe_webhook
)

router = routers.DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'clinics', ClinicViewSet)
router.register(r'reservations', ReservationViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'posts', PostViewSet)
router.register(r'videos', VideoViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'subscriptions', SubscriptionViewSet)
router.register(r'payment-methods', PaymentMethodViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'event-schedules', EventScheduleViewSet)
router.register(r'advertising-campaigns', AdvertisingCampaignViewSet)
router.register(r'users-audit', UsersAuditViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('webhooks/stripe/', stripe_webhook, name='stripe_webhook'),
    path('payments/create-stripe-intent/', CreateStripePaymentIntentView.as_view(), name='create-stripe-intent'),
]
