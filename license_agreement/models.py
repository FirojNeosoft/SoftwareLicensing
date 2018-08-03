from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import RegexValidator


class Address(models.Model):
    """
    Address model
    """
    line1 = models.CharField(max_length=128, blank=True, null=True)
    line2 = models.CharField(max_length=128, blank=True, null=True)
    city_or_village = models.CharField(max_length=128, blank=False, null=False)
    state = models.CharField(max_length=128, blank=False, null=False)
    country = models.CharField(max_length=128, blank=False, null=False)
    zip_code = models.PositiveIntegerField(blank=False, null=False)

    def __str__(self):
        return '%s(%s, %s)' % (self.city_or_village, self.state, self.country)


class Licensor(models.Model):
    """
    Licensor model
    """
    first_name = models.CharField('First Name', max_length=128, blank=False, null=False)
    last_name = models.CharField('Last Name', max_length=128, blank=False, null=False)
    designation = models.CharField('Designation', max_length=128, blank=True, null=True)
    organization_name = models.CharField('Organization', max_length=128, blank=True, null=True)
    address = models.ForeignKey('Address', related_name='licensor', blank=False, null=True, on_delete=models.SET_NULL)
    mobile = models.CharField('Mobile', validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format:\
                                  '+999999999'. Up to 15 digits allowed.")], max_length=15,\
                                  unique=True, blank=False, null=False)
    email = models.EmailField('Email', blank=False, null=False, unique=True)
    status = models.CharField(max_length=10, choices=settings.STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Licensor"

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    @property
    def full_name(self):
        "Returns the licensor's full name."
        return '%s %s' % (self.first_name, self.last_name)

    def delete(self):
        """
        Delete licensor
        """
        self.status = 'Delete'
        self.save()


class Licensee(models.Model):
    """
    Licensee model
    """
    first_name = models.CharField('First Name', max_length=128, blank=False, null=False)
    last_name = models.CharField('Last Name', max_length=128, blank=False, null=False)
    designation = models.CharField('Designation', max_length=128, blank=True, null=True)
    organization_name = models.CharField('Organization', max_length=128, blank=True, null=True)
    address = models.ForeignKey('Address', related_name='licensee', blank=False, null=True, on_delete=models.SET_NULL)
    mobile = models.CharField('Mobile', validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format:\
                                  '+999999999'. Up to 15 digits allowed.")], max_length=15,\
                                  unique=True, blank=False, null=False)
    email = models.EmailField('Email', blank=False, null=False, unique=True)
    status = models.CharField(max_length=10, choices=settings.STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Licensee"

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    @property
    def full_name(self):
        "Returns the licensee's full name."
        return '%s %s' % (self.first_name, self.last_name)

    def delete(self):
        """
        Delete licensee
        """
        self.status = 'Delete'
        self.save()


class Software(models.Model):
    """
    Software model
    """
    name = models.CharField('Name', max_length=128, blank=False, null=False)
    specification = models.TextField(null=True, blank=True)
    user_guide_document = models.FileField('User Guide Document', upload_to='user_guide_docs/',null=True, blank=True)
    indemnity = models.TextField(null=True, blank=True)   #copyright or patent information
    status = models.CharField(max_length=10, choices=settings.STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Software"
        verbose_name_plural = "Softwares"

    def __str__(self):
        return self.name

    def delete(self):
        """
        Delete software
        """
        self.status = 'Delete'
        self.save()


class SoftwareLicenseAgreement(models.Model):
    """
    SoftwareLicenseAgreement model
    """
    effective_date = models.DateField('Start Date', blank=False, null=False)
    licensor = models.ForeignKey('Licensor', related_name='software_license_agreement', blank=False, null=False,\
                                 on_delete=models.CASCADE)
    licensee = models.ForeignKey('Licensee', related_name='software_license_agreement', blank=False, null=False,\
                                 on_delete=models.CASCADE)
    software = models.ForeignKey('Software', related_name='software_license_agreement', blank=False, null=False,\
                                 on_delete=models.CASCADE)

    valid_ip_addresses = models.CharField('Valid IP Addresses', max_length=512, blank=True, null=True,\
                                          help_text="Enter valid comma separated ip addresses.")
    terms_and_conditions = models.TextField(null=False, blank=False)
    limitation_of_liability = models.TextField(null=True, blank=True)
    termination = models.TextField(null=True, blank=True)

    expiry_date = models.DateField('Expiry Date', blank=False, null=False)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=False, null=False, default=0)
    payment_plan = models.TextField(null=True, blank=True)
    no_of_copies = models.PositiveIntegerField(blank=False, null=False)
    delivery_date = models.DateField('Delivery Date', blank=False, null=False)
    warrenty_period = models.PositiveIntegerField(blank=True, null=True)
    maintenance_agreement = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=settings.STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Software License Agreement"
        verbose_name_plural = "Software License Agreements"

    def __str__(self):
        return 'Agreement between %s and %s for %s' % (self.licensor.full_name, self.licensee.full_name, self.software.name)

    def delete(self):
        """
        Delete SoftwareLicenseAgreement
        """
        self.status = 'Delete'
        self.save()
