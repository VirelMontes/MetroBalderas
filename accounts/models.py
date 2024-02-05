from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    home_address = models.ForeignKey('Address', on_delete=models.CASCADE, related_name='%(class)s_user_home_address', blank=True, null=True)
    groups = models.ManyToManyField('auth.Group', related_name='accounts_users', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='accounts_users', blank=True)

class Address(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='%(class)s_home_address')
    line1 = models.CharField(max_length=100)
    line2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)