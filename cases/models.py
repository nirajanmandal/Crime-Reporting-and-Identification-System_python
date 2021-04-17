from django.db import models
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


class CasesModel(models.Model):
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=False, null=True,)
    contact_email = models.EmailField(max_length=100, blank=True, null=True)
    date_of_case = models.DateTimeField(blank=True, null=True)
    contact_number = models.IntegerField(blank=True, null=True)
    image = models.ImageField(blank=False, null=False, upload_to='cases/')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, blank=False, null=False)
    description = models.TextField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.first_name + ' ' + self.last_name


# class Comment(models.Model):
#     news = models.ForeignKey(AddCase, on_delete=models.CASCADE)
#     commenter = models.CharField(max_length=100)
#     email = models.EmailField()
#     comment = models.TextField(max_length=500, blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.commenter
