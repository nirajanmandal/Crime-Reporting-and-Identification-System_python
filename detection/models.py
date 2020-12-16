from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
private_storage = FileSystemStorage(location=settings.PRIVATE_STORAGE_ROOT)


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


class CitizenProfile(models.Model):
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    birth_date = models.DateField()
    address = models.CharField(max_length=100, blank=False, null=False)
    phone_number = models.BigIntegerField(blank=False, null=False)
    nationality = models.CharField(max_length=50, blank=False, null=False)
    citizenship_number = models.BigIntegerField(blank=False, null=False)
    citizen_image = models.ImageField(upload_to='citizens/', null=False, blank=False)
    bio = models.TextField(max_length=255, null=False, blank=False)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class SpottedCitizen(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    birth_date = models.DateField()
    address = models.CharField(max_length=100, blank=False, null=False)
    phone_number = models.BigIntegerField(blank=False, null=False)
    nationality = models.CharField(max_length=50, blank=False, null=False)
    citizenship_number = models.BigIntegerField(blank=False, null=False)
    citizen_image = models.ImageField(upload_to='citizens/', null=False, blank=False)
    bio = models.TextField(max_length=255, null=False, blank=False)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class File(models.Model):
    file = models.FileField(storage=private_storage, blank=False, null=False)
    remark = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
