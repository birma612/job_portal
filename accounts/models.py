
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('employer', 'Employer'),
        ('seeker', 'Job Seeker'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='seeker'
    )

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True
    )

    education = models.CharField(
        max_length=200,
        blank=True
    )

    skills = models.TextField(blank=True)

    professional_summary = models.TextField(blank=True)

    resume = models.FileField(
        upload_to='resumes/',
        blank=True,
        null=True
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
