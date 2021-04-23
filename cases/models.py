from django.db import models
from django.db.models import Q
from django.urls import reverse

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
)

STATUS_CHOICES = (
    ('Wanted', 'Wanted'),
    ('Spotted', 'Spotted'),
    ('Missing', 'Missing'),
    ('Found', 'Found'),
)


class CaseQueryset(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(address__iexact=query)
                         | Q(status__iexact=query) | Q(gender__iexact=query))
            qs = qs.filter(or_lookup).distinct()
        return qs


class CaseManager(models.Manager):
    def get_queryset(self):
        return CaseQueryset(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)


class CasesModel(models.Model):
    first_name = models.CharField(max_length=50, blank=False, null=True)
    last_name = models.CharField(max_length=50, blank=False, null=True)
    address = models.CharField(max_length=100, blank=False, null=True)
    nationality = models.CharField(max_length=50, blank=False, null=True,)
    contact_email = models.EmailField(max_length=100, blank=True, null=True)
    date_of_case = models.DateField(blank=False, null=True)
    contact_number = models.CharField(max_length=13, blank=False, null=True)
    image = models.ImageField(blank=False, null=False, upload_to='cases/')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=False, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, blank=False, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    objects = CaseManager()
