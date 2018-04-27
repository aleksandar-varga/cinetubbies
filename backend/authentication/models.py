from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.serializers import serialize


SYSTEM_ADMIN = ('admin', 'Admin')
THEATER_ADMIN = ('cinema_admin', 'Theater Admin')
FAN_ZONE_ADMIN = ('fan_zone_admin', 'Fan Zone Admin')
USER = ('user', 'User')

ADMIN_ROLES = (
  SYSTEM_ADMIN,
  THEATER_ADMIN,
  FAN_ZONE_ADMIN,
)

ROLES = ADMIN_ROLES + (USER,)

class User(AbstractUser):
  id = models.AutoField(primary_key=True)
  username = models.CharField(max_length=30, unique=True, editable=False)
  password = models.CharField(max_length=255)
  first_name = models.CharField(max_length=30, blank=True)
  last_name = models.CharField(max_length=30, blank=True)
  birth_date = models.DateField(null=True, blank=True)
  role = models.CharField(max_length=20, choices=ROLES, default='user')
  phone = models.CharField(max_length=30, blank=True)
  city = models.CharField(max_length=30, blank=True)
  first_login = models.BooleanField(default=True)

  def is_system_admin(self):
    return self.role == SYSTEM_ADMIN[0]

  def is_theater_admin(self):
    return self.role == THEATER_ADMIN[0]

  def is_fan_zone_admin(self):
    return self.role == FAN_ZONE_ADMIN[0]

class TheaterAdmin(User):
  theater = models.ForeignKey(
    to='theaters.Theater',
    on_delete=models.SET_NULL,
    related_name='admins',
    null=True,
  )

  def is_system_admin(self):
    return False

  def is_theater_admin(self):
    return True

  def is_fan_zone_admin(self):
    return False

  def __str__(self):
    return serialize('json', [self])[1:-1]

