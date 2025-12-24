from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from users.models import Profile
from .models import Student

@receiver(post_save, sender=User)
def create_user_related_objects(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        # Only create Student if it doesn't exist
        Student.objects.get_or_create(profile=profile)