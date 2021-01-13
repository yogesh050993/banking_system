from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True, verbose_name='username')
    email    = models.EmailField(unique=True, verbose_name='Email')

    mobile_no    = models.CharField(max_length=15, default='', verbose_name='Mobile Number')
    first_name   = models.CharField(max_length=150, verbose_name='First Name')
    last_name    = models.CharField(max_length=150, default='', verbose_name='Last Name')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name='Updated At')

    class Meta:
        db_table = 'user_master'
        verbose_name = 'User'
        verbose_name_plural = 'User Master'

    def __str__(self):
        return self.email

