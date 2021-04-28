from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
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


class CitizenProfileQueryset(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(
                status__iexact=query) | Q(gender__iexact=query))
            qs = qs.filter(or_lookup).distinct()
        return qs


class CitizenProfileManager(models.Manager):
    def get_queryset(self):
        return CitizenProfileQueryset(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)


class CitizenProfile(models.Model):
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    birth_date = models.DateField()
    address = models.CharField(max_length=100, blank=False, null=False)
    phone_number = models.CharField(max_length=13, blank=False, null=False)
    nationality = models.CharField(max_length=50, blank=False, null=False)
    citizenship_number = models.CharField(max_length=20, blank=False, null=False)
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

    objects = CitizenProfileManager()


class SpottedCitizen(models.Model):
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    location = models.CharField(max_length=50, blank=False, null=True)
    date_of_spotted = models.DateTimeField(blank=False, null=True)
    image = models.ImageField(upload_to='spotted/', null=False, blank=False)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES)
    description = models.TextField(max_length=255, null=False, blank=False)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.first_name + ' ' + self.last_name

