from django.db import models
from profiles.models import UserProfile


import uuid

# Create your models here.


class Enquiry(models.Model):
    """
    A model for handling user enquiries.
    """

    class Meta:
        verbose_name_plural = 'Enquiries'

    ENQUIRY_STATUS = (
        ('unresolved', 'Unresolved'),
        ('resolved', 'Resolved')
    )

    enquiry_number = models.CharField(max_length=32, null=False,
                                      editable=False)
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='enquiries'
    )
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    enquiry_subject = models.CharField(max_length=255, null=False, blank=False)
    enquiry_message = models.TextField(null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    def _generate_enquiry_number(self):
        """
        Generate a random, unique enquiry number using UUID.
        """
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        """
        Override the save method to set
        the enquiry number if it hasn't been set.
        """
        if not self.enquiry_number:
            self.enquiry_number = self._generate_enquiry_number()
        super().save(*args, **kwargs)
