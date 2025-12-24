from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    image = models.ImageField(default='profile_pics/default.png', upload_to='profile_pics')
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'