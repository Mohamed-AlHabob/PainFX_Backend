from rest_framework import serializers
from apps.authentication.models import User, Patient, Doctor, UserProfile, Specialization

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'phone_number','address','gander', 'html_content', 'json_content', 'avatar', 'longitude','latitude']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(source='userprofile', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email','role', 'first_name', 'last_name', 'is_active', 'is_staff', 
                  'date_joined', 'last_login', 'profile']

# Patient Serializer
class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Patient
        fields = ["user", "medical_history"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        return Patient.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)
        if user_data:
            user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        instance.medical_history = validated_data.get("medical_history", instance.medical_history)
        instance.save()
        return instance

class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ['id', 'name']
        
class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    specialization = SpecializationSerializer()

    class Meta:
        model = Doctor
        fields = ["user", "specialization", "license_number", "reservation_open"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        specialization_data = validated_data.pop("specialization", None)

        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        specialization = Specialization.objects.get_or_create(**specialization_data)[0]

        return Doctor.objects.create(user=user, specialization=specialization, **validated_data)

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)
        specialization_data = validated_data.pop("specialization", None)

        if user_data:
            user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        if specialization_data:
            specialization = Specialization.objects.get_or_create(**specialization_data)[0]
            instance.specialization = specialization

        instance.license_number = validated_data.get("license_number", instance.license_number)
        instance.reservation_open = validated_data.get("reservation_open", instance.reservation_open)
        instance.save()
        return instance
