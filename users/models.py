
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import date
from django.contrib.auth.models import Group, Permission

# Create your models here.
class UserAgent(AbstractUser):
  PROFIL = (
        ('ADMIN', 'ADMIN'),
        ('INVENTORY', 'INVENTORY'),
        ('MAINTENANCE', 'MAINTENANCE'),
        # Add all the other currencies here
    )
  username = models.CharField(max_length = 50, blank = True)
  email = models.EmailField('email address', unique = True)
  poste = models.CharField(max_length = 50, blank = True, null = True)
  profil = models.CharField(max_length=20, choices=PROFIL)
  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = ['username','password']
  def __str__(self):
      return "{} - {}".format(self.username,self.email)

  groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name="users_groups",
        related_query_name="user",
        help_text=
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ,
    )

  user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name="users_permissions",
        related_query_name="user",
        help_text='Specific permissions for this user.',
    )