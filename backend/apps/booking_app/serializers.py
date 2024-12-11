# backend/booking_app/serializers.py

from rest_framework import serializers
from apps.booking_app.models import (
    Clinic,
    Reservation,
    ReservationStatus, Review, Post,
    Comment, Like, Category, Subscription, PaymentMethod,
    Payment, Notification, EventSchedule, AdvertisingCampaign,
    UsersAudit,Tag
)

from apps.authentication.serializers import DoctorSerializer, UserSerializer,PatientSerializer,SpecializationSerializer

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']
        read_only_fields = ['id', 'created_at']

# Clinic Serializer
class ClinicSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    doctors = DoctorSerializer(many=True)
    specialization = SpecializationSerializer()
    class Meta:
        model = Clinic
        fields = ['id','name', 'address','doctors','icon','owner','specialization', 'description','reservation_open','privacy','active','license_number','license_expiry_date','created_at', 'updated_at']
        write_only_fields= ['id','owner','doctors']


class ReservationSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = ['id','clinic','status','reason_for_cancellation','reservation_date','reservation_time','patient','doctor']

    def create(self, validated_data):
        """
        Override the create method to set the patient field to the current user.
        """
        user = self.context['request'].user
        if not hasattr(user, 'patient'):
            raise serializers.ValidationError("Only patients can create reservations.")
        # Add the patient instance to the validated data
        validated_data['patient'] = user.patient
        return super().create(validated_data)

# Review Serializer
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['clinic', 'rating', 'review_text']
        read_only_fields = ['id', 'patient', 'created_at']

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
    
# # Video Serializer
# class VideoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Video
#         fields = ['id', 'video_file', 'video_url', 'thumbnail_url']
#         read_only_fields = ['id', 'video_url', 'thumbnail_url']

#     def validate(self, attrs):
#         post = attrs.get('post')
#         if post.type != PostType.VIDEO:
#             raise serializers.ValidationError('Post type must be VIDEO to attach a video.')
#         return attrs

# Post Serializer
class PostSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'video_file', 'video_url','thumbnail_url', 'content',
            'doctor', 'likes_count', 'comments_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'doctor', 'likes_count', 'comments_count', 'created_at', 'updated_at']

    def create(self, validated_data):
        user = self.context['request'].user
        if not hasattr(user, 'doctor'):
            raise serializers.ValidationError("Only doctors can create posts.")
        validated_data['doctor'] = user.doctor
        return super().create(validated_data)

# Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post',  'comment_text', 'parent_comment']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
        

# Like Serializer
class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Like
        fields = ['id', 'post','user', 'created_at', 'updated_at']

# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

# Subscription Serializer
class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = [ 'category', 'status', 'payment']
        read_only_fields = ['id','user', 'created_at', 'updated_at']

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
