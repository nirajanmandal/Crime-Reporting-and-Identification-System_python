from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

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
            or_lookup = (Q(case_first_name__icontains=query) | Q(case_last_name__icontains=query)
                         | Q(address__iexact=query)
                         | Q(status__iexact=query) | Q(gender__iexact=query))
            qs = qs.filter(or_lookup).distinct()
        return qs


class CaseManager(models.Manager):
    def get_queryset(self):
        return CaseQueryset(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)


class CasesModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100, blank=False, null=True)
    case_first_name = models.CharField(max_length=50, blank=False, null=True)
    case_last_name = models.CharField(max_length=50, blank=False, null=True)
    case_location = models.CharField(max_length=50, blank=False, null=True)
    date_of_case = models.DateTimeField(blank=False, null=True)
    image = models.ImageField(blank=False, null=False, upload_to='cases/')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, blank=False, null=False)
    case_description = models.TextField(max_length=500, blank=True, null=True)

    reporter_first_name = models.CharField(max_length=50, blank=False, null=True)
    reporter_last_name = models.CharField(max_length=50, blank=False, null=True)
    address = models.CharField(max_length=100, blank=False, null=True)
    contact_email = models.EmailField(max_length=100, blank=True, null=True)
    contact_number = models.CharField(max_length=14, blank=False, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    reporter_description = models.TextField(max_length=500, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.title

    objects = CaseManager()
