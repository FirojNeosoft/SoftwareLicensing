from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import RegexValidator


class SMS(models.Model):
    """
    SMS model
    """
    mobile = models.CharField('Mobile', validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$',\
                                 message="Phone number must be entered in the format:\
                                  '+999999999'. Up to 15 digits allowed.")], max_length=15,\
                                  unique=True, blank=False, null=False)
    message = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=settings.MESSAGE_STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "SMS"

    def __str__(self):
        return self.mobile

    def delete(self):
        """
        Delete SMS
        """
        self.status = 'Delete'
        self.save()
