from django.db import models
from authentication.models import User
from theaters.models import Theater

class Movie(models.Model):
  id = models.AutoField(primary_key=True)
  title = models.CharField(max_length=255, blank=False)
  genre = models.CharField(max_length=255, blank=False)
  director = models.CharField(max_length=255, blank=True)
  actors = models.CharField(max_length=255, blank=True)
  duration = models.CharField(max_length=255, blank=True)
  description = models.CharField(max_length=255, blank=True)
  theater = models.ForeignKey(Theater, on_delete=models.PROTECT, null=True, related_name='movies')

  class Meta:
    db_table = 'movies'
