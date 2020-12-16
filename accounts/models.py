from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
)

STATUS_CHOICES = (
    ('Free', 'Free'),
    ('Wanted', 'Wanted'),
    ('Missing', 'Missing'),
    ('Found', 'Found'),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    profile_image = models.ImageField(upload_to='citizens/', null=False, blank=False)
    nationality = models.CharField(max_length=50, null=False, blank=False)
    citizenship_number = models.CharField(max_length=50, null=False, blank=False)
    phone_number = models.BigIntegerField(null=False, blank=False)
    address = models.CharField(max_length=50, null=False, blank=False)
    bio = models.TextField(max_length=500, null=False, blank=False)
    birth_date = models.DateField(null=False, blank=False)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=False, blank=False)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)



