# backend/booking_app/serializers.py

from rest_framework import serializers
from apps.booking_app.models import (
    Clinic,
    ClinicDoctor,
    PostType,
    Reservation,
    ReservationStatus, Review, Post, Video,
    Comment, Like, Category, Subscription, PaymentMethod,
    Payment, Notification, EventSchedule, AdvertisingCampaign,
    UsersAudit,Tag
)
from apps.authentication.models import Doctor, User
from apps.authentication.serializers import DoctorSerializer, UserSerializer

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'created_at']

# Clinic Serializer
class ClinicSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    doctors = DoctorSerializer(many=True)

    class Meta:
        model = Clinic
        fields = (
            'id',
            'name',
            'address',
            'owner',
            'doctors',
            'created_at',
            'updated_at',
            'geolocation',
        )

    def create(self, validated_data):
        owner_data = validated_data.pop('owner')
        doctors_data = validated_data.pop('doctors')

        # Create or get the owner user
        owner, _ = User.objects.get_or_create(
            email=owner_data.get('email'),
            defaults={
                'first_name': owner_data.get('first_name'),
                'last_name': owner_data.get('last_name'),
                'role': owner_data.get('role', 'admin'),
            }
        )

        clinic = Clinic.objects.create(owner=owner, **validated_data)

        # Handle the ManyToMany relationship with doctors
        for doctor_data in doctors_data:
            user_data = doctor_data.pop('user')
            doctor_user, _ = User.objects.get_or_create(
                email=user_data.get('email'),
                defaults={
                    'first_name': user_data.get('first_name'),
                    'last_name': user_data.get('last_name'),
                    'role': user_data.get('role', 'doctor'),
                }
            )
            doctor, _ = Doctor.objects.get_or_create(user=doctor_user, **doctor_data)
            ClinicDoctor.objects.get_or_create(clinic=clinic, doctor=doctor)

        return clinic

    def update(self, instance, validated_data):
        owner_data = validated_data.pop('owner', None)
        doctors_data = validated_data.pop('doctors', None)

        # Update clinic fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update owner information if provided
        if owner_data:
            owner = instance.owner
            for attr, value in owner_data.items():
                setattr(owner, attr, value)
            owner.save()

        # Update doctors if provided
        if doctors_data:
            # Clear existing relationships
            instance.doctors.clear()
            for doctor_data in doctors_data:
                user_data = doctor_data.pop('user')
                doctor_user, _ = User.objects.get_or_create(
                    email=user_data.get('email'),
                    defaults={
                        'first_name': user_data.get('first_name'),
                        'last_name': user_data.get('last_name'),
                        'role': user_data.get('role', 'doctor'),
                    }
                )
                doctor, _ = Doctor.objects.get_or_create(user=doctor_user, **doctor_data)
                ClinicDoctor.objects.get_or_create(clinic=instance, doctor=doctor)

        return instance


# Reservation Serializer
class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'patient', 'clinic', 'status', 'reason_for_cancellation',
                  'reservation_date', 'reservation_time', 'created_at', 'updated_at']

    def validate(self, attrs):
        if attrs.get('created_at') and attrs.get('updated_at') and attrs['created_at'] > attrs['updated_at']:
            raise serializers.ValidationError("created_at must be before or equal to updated_at")
        return attrs

# Review Serializer
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'clinic', 'patient', 'rating', 'review_text', 'created_at']

    def validate(self, attrs):
        patient = attrs.get('patient')
        clinic = attrs.get('clinic')
        if not Reservation.objects.filter(
            patient=patient,
            clinic=clinic,
            status=ReservationStatus.APPROVED
        ).exists():
            raise serializers.ValidationError('Patient must have an approved reservation at the clinic to leave a review')
        return attrs

# Post Serializer
class PostSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()
    class Meta:
        model = Post
        fields = ['id', 'doctor','title','html_content','json_content', 'content', 'type', 'created_at', 'updated_at']

    def validate(self, attrs):
        doctor = attrs.get('doctor')
        if not Doctor.objects.filter(user=doctor.user).exists():
            raise serializers.ValidationError('Only doctors can create posts')
        return attrs

# Video Serializer
class VideoSerializer(serializers.ModelSerializer):
    post = PostSerializer()
    class Meta:
        model = Video
        fields = ['id', 'post','video_file', 'video_url', 'thumbnail_url']

    def validate(self, attrs):
        post = attrs.get('post')
        if post.type != PostType.VIDEO:
            raise serializers.ValidationError('Post type must be video')
        return attrs

# Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'comment_text', 'parent_comment', 'created_at']

# Like Serializer
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'post', 'user', 'created_at']

# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

# Subscription Serializer
class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'category', 'status', 'payment', 'created_at', 'updated_at']

# PaymentMethod Serializer
class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ['id', 'method_name']

# Payment Serializer
class PaymentSerializer(serializers.ModelSerializer):
    subscription = SubscriptionSerializer()
    reservation = ReservationSerializer()
    method = PaymentMethodSerializer()
    class Meta:
        model = Payment
        fields = ['id', 'user', 'amount', 'method', 'payment_status', 'subscription', 'reservation', 'created_at']

    def validate(self, attrs):
        subscription = attrs.get('subscription')
        reservation = attrs.get('reservation')
        if bool(subscription) == bool(reservation):
            raise serializers.ValidationError('Payment must be associated with either a subscription or a reservation, but not both.')
        return attrs

# Notification Serializer
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'is_read', 'created_at']

# EventSchedule Serializer
class EventScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventSchedule
        fields = ['id', 'clinic', 'doctor', 'event_name', 'start_time', 'end_time', 'description']

    def validate(self, attrs):
        if attrs['start_time'] >= attrs['end_time']:
            raise serializers.ValidationError('start_time must be before end_time')
        return attrs

# AdvertisingCampaign Serializer
class AdvertisingCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisingCampaign
        fields = ['id', 'clinic', 'campaign_name', 'start_date', 'end_date', 'budget', 'status']

    def validate(self, attrs):
        if attrs['start_date'] > attrs['end_date']:
            raise serializers.ValidationError('start_date must be before or equal to end_date')
        return attrs

# UsersAudit Serializer
class UsersAuditSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersAudit
        fields = ['id', 'user', 'changed_data', 'changed_at']
