from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from users.models import Profile

# Create your models here.
class Issue(models.Model):
    type = models.CharField(
        max_length=100,
        choices=[('Hardware', 'Hardware'), ('Software', 'Software')]
    )
    room = models.CharField(max_length=100)
    urgent = models.BooleanField(default=False)
    details = models.TextField()
    date_submitted = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    author = models.ForeignKey(
        User,
        related_name='issues',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.type} Issue in {self.room}'

    def get_absolute_url(self):
        return reverse('itreporting:issue-detail', kwargs={'pk': self.pk})

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.code} - {self.name}"
    
class Module(models.Model):
    CATEGORY_CHOICES = [
        ("CORE", "Core"),
        ("OPTIONAL", "Optional"),
    ]    
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    students = models.ManyToManyField(Student, blank=True)
    is_open = models.BooleanField(default=True)
    credit = models.IntegerField()
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    description = models.TextField()
    courses = models.ManyToManyField(Course, related_name="modules")

    def __str__(self):
        return f"{self.code} – {self.name}"