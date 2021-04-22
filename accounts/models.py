from django.db import models
from django.contrib.auth.models import User

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    profile_image = models.ImageField(upload_to='citizens/', null=False, blank=False, default='assets/img/default-avatar.png')
    nationality = models.CharField(max_length=50, null=False, blank=False)
    citizenship_number = models.CharField(max_length=50, null=False, blank=False)
    phone_number = models.CharField(max_length=13, null=False, blank=False)
    address = models.CharField(max_length=50, null=False, blank=False)
    bio = models.TextField(max_length=500, null=False, blank=False)
    birth_date = models.DateField(null=False, blank=False)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)
