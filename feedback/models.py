from django.db import models
from django.contrib.auth.models import User
from cases.models import CasesModel


class FeedbackModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    case = models.ForeignKey(CasesModel, on_delete=models.SET_NULL, null=True)
    email = models.EmailField(max_length=30, blank=False, null=False)
    subject = models.CharField(max_length=50, blank=False, null=False)
    message = models.TextField(max_length=500, blank=False, null=False)
    image = models.ImageField(upload_to='feedback/', null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
