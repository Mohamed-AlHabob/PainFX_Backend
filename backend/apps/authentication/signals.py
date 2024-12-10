from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.authentication.models import User, UserProfile, Patient

# Signal to automatically create UserProfile and Patient instances
@receiver(post_save, sender=User)
def create_user_related_models(sender, instance, created, **kwargs):
    if created:
        # Create UserProfile for every new user
        UserProfile.objects.create(user=instance)
        
        # Create Patient if the user's role is 'patient'
        if instance.role == 'patient':
            Patient.objects.create(user=instance)
