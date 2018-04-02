from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.fields import RandomCharField


class Payment(models.Model):
    STATE_CREATED = 'created'
    STATE_OPENED = 'opened'
    STATE_BANK = 'bank'
    STATE_SUCCESS = 'successful'
    STATE_FAILURE = 'unsuccessful'
    STATE_CHOICES = (
        (STATE_CREATED, 'Created'),
        (STATE_OPENED, 'Opened'),
        (STATE_BANK, 'Sent to bank'),
        (STATE_SUCCESS, 'Successful payment'),
        (STATE_FAILURE, 'Unsuccessful payment')
    )

    price = models.PositiveIntegerField()
    token = models.CharField(max_length=500, unique=True, null=True, blank=True)
    slug = RandomCharField(length=8, unique=True)
    trace_number = RandomCharField(length=8, unique=True, include_alpha=False)
    state = models.CharField(max_length=30, choices=STATE_CHOICES, default=STATE_CREATED)
    payment_result = models.CharField(max_length=256, null=True, blank=True)
    verification_result = models.CharField(max_length=256, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    gateway = models.CharField(max_length=256, null=True)
    description = models.CharField(max_length=1024, null=True)
    login_required = models.BooleanField(default=False)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    ref_number = models.CharField(max_length=200, null=True, unique=True)

    # Returning user to your website
    callable_module = models.CharField(max_length=300, null=True)
    callable_name = models.CharField(max_length=100, null=True)
    return_url = models.CharField(max_length=1024, null=True)

    def verification_done(self):
        return self.state in [self.STATE_SUCCESS, self.STATE_FAILURE]

    def successful(self):
        return self.state == self.STATE_SUCCESS

    class Meta:
        app_label = 'pardakht'
