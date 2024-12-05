from django.contrib import admin
from apps.authentication.models import User , UserProfile , Doctor, Patient,Specialization
# Register your models here.
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Specialization)
admin.site.register(Doctor)
admin.site.register(Patient)